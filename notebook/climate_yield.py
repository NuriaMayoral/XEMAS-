"""XEMA weather -> comarca climate anomalies -> crop-yield anomalies -> regression.

Steps (each one a function):
  download_daily / download_stations   Socrata API, paged by year
  monthly_station                      station x variable x month (needs >= MIN_DAYS valid days)
  comarca_monthly                      anomalies per station first, then averaged per comarca
  seasonal                             anomalies over a crop-specific window of months
  yield_anomaly                        detrended log-yield per comarca x crop
  fit                                  pooled OLS per crop, errors clustered by comarca and year
Equations:  ln y_{c,t} = a_c + b_c t + e_{c,t}        (e = relative yield anomaly)
            e_{c,t}   = b_T dT_{c,t} + b_P dP_{c,t}/Pbar_c + u_{c,t}
"""
import numpy as np
import pandas as pd
import requests

URL_DAILY = "https://analisi.transparenciacatalunya.cat/resource/7bvh-jvq2.json"
URL_STATIONS = "https://analisi.transparenciacatalunya.cat/resource/yqwd-vj5e.json"
MIN_DAYS = 25          # valid days needed to accept a station-month
PAGE = 50000

# crop -> (window name); window = (first month, last month, starts in previous year?)
WINDOWS = {"cereal": (10, 6, True),     # sowing in autumn -> harvest in June
           "growing": (4, 9, False),    # maize, vine
           "tree": (2, 9, False)}       # almond, olive: flowering -> fruit filling
CROP_WINDOW = {"Blat": "cereal", "Ordi": "cereal", "Blat de moro": "growing",
               "Ametller": "tree", "Olivera": "tree", "Vinya de raïm per a vi": "growing"}


# ------------------------------------------------------------------ download
def _get(url, params):
    out, offset = [], 0
    while True:
        p = dict(params, **{"$limit": PAGE, "$offset": offset})
        r = requests.get(url, params=p, timeout=120)
        r.raise_for_status()
        rows = r.json()
        out += rows
        if len(rows) < PAGE:
            return out
        offset += PAGE


def download_daily(y0=2008, y1=2025):
    """Daily mean temperature (1000) and precipitation (1300), one request series per year."""
    frames = []
    for y in range(y0, y1 + 1):
        rows = _get(URL_DAILY, {
            "$select": "data_lectura, codi_estacio, codi_variable, valor",
            "$where": f"codi_variable in('1000','1300') and data_lectura >= '{y}-01-01T00:00:00' "
                      f"and data_lectura < '{y + 1}-01-01T00:00:00'",
            "$order": "data_lectura, codi_estacio, codi_variable"})
        d = pd.DataFrame(rows)
        print(y, len(d))
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["data_lectura"] = pd.to_datetime(d["data_lectura"])
    d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
    d["codi_variable"] = d["codi_variable"].astype(str)
    return d


def download_stations():
    s = pd.DataFrame(_get(URL_STATIONS, {"$select": "codi_estacio, nom_comarca", "$order": "codi_estacio"}))
    return s


# ------------------------------------------------------------------- monthly
def monthly_station(daily):
    d = daily.dropna(subset=["valor"]).copy()
    d["year"], d["month"] = d["data_lectura"].dt.year, d["data_lectura"].dt.month
    g = d.groupby(["codi_estacio", "codi_variable", "year", "month"])["valor"]
    m = g.agg(["mean", "sum", "count"]).reset_index()
    m = m[m["count"] >= MIN_DAYS]
    m["v"] = np.where(m["codi_variable"] == "1000", m["mean"], m["sum"])   # T: mean, P: monthly total
    m["var"] = m["codi_variable"].map({"1000": "T", "1300": "P"})
    return m[["codi_estacio", "var", "year", "month", "v"]]


def comarca_monthly(mst, stations, fix_comarca, min_years=10):
    """Anomalies are computed per station (own monthly climatology), then averaged per comarca,
    so stations that open or close do not create fake trends."""
    st = stations.assign(comarca=stations["nom_comarca"].map(fix_comarca))[["codi_estacio", "comarca"]]
    m = mst.merge(st, on="codi_estacio", how="inner")
    key = ["codi_estacio", "var", "month"]
    m["clim"] = m.groupby(key)["v"].transform("mean")
    m["nyr"] = m.groupby(key)["v"].transform("count")
    m = m[m["nyr"] >= min_years].copy()
    m["anom"] = m["v"] - m["clim"]
    g = m.groupby(["comarca", "var", "year", "month"])[["anom", "clim"]].mean().reset_index()
    w = g.pivot_table(index=["comarca", "year", "month"], columns="var", values=["anom", "clim"])
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    return w.reset_index()      # anom_T, anom_P, clim_T, clim_P


# ------------------------------------------------------------------ seasonal
def seasonal(cm, window):
    """Anomalies of a window of months for each comarca and crop year."""
    m0, m1, prev = WINDOWS[window]
    c = cm.copy()
    if prev:    # months m0..12 belong to the next crop year
        c["cy"] = np.where(c["month"] >= m0, c["year"] + 1, c["year"])
        c = c[(c["month"] >= m0) | (c["month"] <= m1)]
    else:
        c["cy"] = c["year"]
        c = c[(c["month"] >= m0) & (c["month"] <= m1)]
    nmon = (m1 - m0 + 1) if not prev else (12 - m0 + 1 + m1)
    g = c.groupby(["comarca", "cy"]).agg(dT=("anom_T", "mean"), dP=("anom_P", "sum"),
                                        Pclim=("clim_P", "sum"), n=("month", "nunique")).reset_index()
    g = g[g["n"] == nmon]                              # complete windows only
    g["dP_rel"] = g["dP"] / g["Pclim"]
    return g.rename(columns={"cy": "year"})[["comarca", "year", "dT", "dP_rel"]]


# --------------------------------------------------------------------- yield
def yield_anomaly(h, crops=None, min_years=10, min_area=300):
    """h = idescat_loader.harmonise(df). Relative anomaly e = residual of ln(yield) ~ a + b*year."""
    crops = crops or list(CROP_WINDOW)
    d = h[h["crop_h"].isin(crops) & (h["yield_prod_kg_ha"] > 0) & (h["area_total_ha"] > 0)].copy()
    d = d[d.groupby(["comarca", "crop_h"])["area_total_ha"].transform("mean") >= min_area]
    d = d[d.groupby(["comarca", "crop_h"])["year"].transform("count") >= min_years]
    out = []
    for (c, k), g in d.groupby(["comarca", "crop_h"]):
        y = np.log(g["yield_prod_kg_ha"].to_numpy())
        b, a = np.polyfit(g["year"].to_numpy(), y, 1)
        out.append(g.assign(e=y - (a + b * g["year"]), trend_pct=100 * b))
    return pd.concat(out, ignore_index=True)


# ----------------------------------------------------------------------- fit
def fit(ya, cm):
    """Pooled OLS per crop with errors clustered by comarca and year. Returns a summary table + the data."""
    import statsmodels.formula.api as smf
    rows, data = [], []
    for crop, win in CROP_WINDOW.items():
        s = seasonal(cm, win)
        d = ya[ya["crop_h"] == crop].merge(s, on=["comarca", "year"])
        if len(d) < 30:
            continue
        # the same year hits every comarca: cluster by comarca AND year (otherwise p-values are far too small)
        g = np.column_stack([pd.factorize(d["comarca"])[0], d["year"].to_numpy()])
        r = smf.ols("e ~ dT + dP_rel", d).fit(cov_type="cluster", cov_kwds={"groups": g})
        ci = r.conf_int()                      # 95 % interval
        rows.append({"crop": crop, "window": win, "n": int(r.nobs), "n_comarques": d["comarca"].nunique(),
                     "b_T_pct_per_C": 100 * r.params["dT"], "p_T": r.pvalues["dT"],
                     "b_T_lo": 100 * ci.loc["dT", 0], "b_T_hi": 100 * ci.loc["dT", 1],
                     "b_P_pct_per_100pct": 100 * r.params["dP_rel"], "p_P": r.pvalues["dP_rel"],
                     "b_P_lo": 100 * ci.loc["dP_rel", 0], "b_P_hi": 100 * ci.loc["dP_rel", 1],
                     "R2": r.rsquared})
        data.append(d.assign(crop_h=crop))
    return pd.DataFrame(rows), pd.concat(data, ignore_index=True)
