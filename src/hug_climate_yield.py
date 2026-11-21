"""This file is used as a function repository for the main jupiter notebook
The goal is to be able to load all data from XEMA database (see URL_DAILY and
URL_STATIONS). Because all colaborators will use this databases, the functions 
to download the data may be reused by them.

I did overextend and di some of the mixing between the crop and weather datasets,
but it came handy given all the weather data processing.
"""

import numpy as np
import pandas as pd
import requests

URL_DAILY = "https://analisi.transparenciacatalunya.cat/resource/7bvh-jvq2.json"
URL_STATIONS = "https://analisi.transparenciacatalunya.cat/resource/yqwd-vj5e.json"
MIN_DAYS = 25          # valid days needed to accept a station-month
PAGE = 50000

# We characterize the season of growth on each type of crop. True if they span over 2 different years:
WINDOWS = {"cereal": (10, 6, True),     # sowing in autumn and harvest in June
           "growing": (4, 9, False),    # maize, vine
           "tree": (2, 9, False)}       # almond, olive: flowering and fruit filling
CROP_WINDOW = {"Blat": "cereal", "Ordi": "cereal", "Blat de moro": "growing",
               "Ametller": "tree", "Olivera": "tree", "Vinya de raïm per a vi": "growing"} # classify in the groups of seasons 


def _get(url, params):
    """This function accesses the API and requests the data asked through a SQL command, row 
    limit and offset in the parameters through dictionary params"""
    out, offset = [], 0
    while True:
        p = dict(params, **{"$limit": PAGE, "$offset": offset})
        r = requests.get(url, params=p, timeout=120)
        r.raise_for_status()
        rows = r.json()
        out += rows
        if len(rows) < PAGE: #row limit
            return out
        offset += PAGE


def download_daily(y0=2008, y1=2025):
    """This function downloads the daily mean temperature (code=1000) and precipitation (code=1300), one request series per 
    year, from the first dataset (URL_DAILY)."""
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
    """This functions downloads from the API the data of every station and region"""
    s = pd.DataFrame(_get(URL_STATIONS, {"$select": "codi_estacio, nom_comarca", "$order": "codi_estacio"}))
    return s



def monthly_station(daily):
    """This function turns the daily data into one value per per station, variable, year and month format"""
    d = daily.dropna(subset=["valor"]).copy() # we drop missing data
    d["year"], d["month"] = d["data_lectura"].dt.year, d["data_lectura"].dt.month
    g = d.groupby(["codi_estacio", "codi_variable", "year", "month"])["valor"]
    m = g.agg(["mean", "sum", "count"]).reset_index()
    m = m[m["count"] >= MIN_DAYS]
    m["v"] = np.where(m["codi_variable"] == "1000", m["mean"], m["sum"]) # Relate the code_variable to the actual variable 
    m["var"] = m["codi_variable"].map({"1000": "T", "1300": "P"})
    return m[["codi_estacio", "var", "year", "month", "v"]]


def comarca_monthly(mst, stations, fix_comarca, min_years=10):
    """This function takes the monthly table from previous function and computes the anomalies per station: 
    how far is the rain/temperature of this month from average. Also links the station locations to the comarques"""
    st = stations.assign(comarca=stations["nom_comarca"].map(fix_comarca))[["codi_estacio", "comarca"]] # Assign comarca to station
    m = mst.merge(st, on="codi_estacio", how="inner")
    key = ["codi_estacio", "var", "month"]
    m["clim"] = m.groupby(key)["v"].transform("mean") # we compute each station's mean
    m["nyr"] = m.groupby(key)["v"].transform("count")
    m = m[m["nyr"] >= min_years].copy() # We count the number of years we can average months, if it's under 10, drop it
    m["anom"] = m["v"] - m["clim"] # the anomaly is value measured minus the mean
    g = m.groupby(["comarca", "var", "year", "month"])[["anom", "clim"]].mean().reset_index() # And we average over the all anomalies in the comarca
    w = g.pivot_table(index=["comarca", "year", "month"], columns="var", values=["anom", "clim"])
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    return w.reset_index() #new shape: anom_T, anom_P, clim_T, clim_P



def seasonal(cm, window):
    """This function uses the previous to convert the anomalies into rain anomalies and temperature anomalies for
    a certain crop in a window of months for each comarca and year. If a crop starts on one year and it's harvested 
    on the following one, the yield is accounted to the harvesting year"""

    m0, m1, prev = WINDOWS[window] # we take the months of the window and if the season starts in one year and ends on the next
    c = cm.copy()
    if prev:   
        c["cy"] = np.where(c["month"] >= m0, c["year"] + 1, c["year"])
        c = c[(c["month"] >= m0) | (c["month"] <= m1)] # We have to asign the first month to one year and the las to the following
    else:
        c["cy"] = c["year"]
        c = c[(c["month"] >= m0) & (c["month"] <= m1)]
    nmon = (m1 - m0 + 1) if not prev else (12 - m0 + 1 + m1) # The number of months 
    g = c.groupby(["comarca", "cy"]).agg(dT=("anom_T", "mean"), dP=("anom_P", "sum"),
                                        Pclim=("clim_P", "sum"), n=("month", "nunique")).reset_index() # Aggregate per comarca per year
    g = g[g["n"] == nmon] # complete windows only
    g["dP_rel"] = g["dP"] / g["Pclim"] # relative rain anomaly
    return g.rename(columns={"cy": "year"})[["comarca", "year", "dT", "dP_rel"]]



def yield_anomaly(h, crops=None, min_years=10, min_area=300):
    """This function uses the harmonise function to to remove the trend of the yield only to leave with deviations do to the weather
    Relative anomaly d = residual of ln(yield) ~ a + b*year."""
    crops = crops or list(CROP_WINDOW)
    d = h[h["crop_h"].isin(crops) & (h["yield_prod_kg_ha"] > 0) & (h["area_total_ha"] > 0)].copy()
    d = d[d.groupby(["comarca", "crop_h"])["area_total_ha"].transform("mean") >= min_area] # we have to remove very small areas (too noisy)
    d = d[d.groupby(["comarca", "crop_h"])["year"].transform("count") >= min_years] # Also we require a minimum of 10 years for the series
    out = []
    for (c, k), g in d.groupby(["comarca", "crop_h"]): # we fit the trend of the crop data to discount the tech evolution only to leave the weather anomaly
        y = np.log(g["yield_prod_kg_ha"].to_numpy())
        b, a = np.polyfit(g["year"].to_numpy(), y, 1)
        out.append(g.assign(e=y - (a + b * g["year"]), trend_pct=100 * b))
    return pd.concat(out, ignore_index=True)


def fit(ya, cm, verbose = True):
    """This function uses the previous to compute d anomalies, to compute how a crop is influenced by rain and temperature anomalies. 
    Pooled OLS per crop with errors clustered by comarca and year. Returns a summary table + the data."""
    import statsmodels.formula.api as smf # type: ignore
    rows, data = [], []
    for crop, win in CROP_WINDOW.items(): # Each selected crops gets its regression and window
        s = seasonal(cm, win) # we compute the anomalies and add them into the crop data per year
        d = ya[ya["crop_h"] == crop].merge(s, on=["comarca", "year"])
        if len(d) < 30: # the observations must be sufficient 
            continue
        g = np.column_stack([pd.factorize(d["comarca"])[0], d["year"].to_numpy()])
        r = smf.ols("e ~ dT + dP_rel", d).fit(cov_type="cluster", cov_kwds={"groups": g}) # For all comarques and years, fit one regression per crop, through OLS
        ci = r.conf_int() # confidence interval
        rows.append({"crop": crop, "window": win, "n": int(r.nobs), "n_comarques": d["comarca"].nunique(),
                     "b_T_pct_per_C": 100 * r.params["dT"], "p_T": r.pvalues["dT"],
                     "b_T_lo": 100 * ci.loc["dT", 0], "b_T_hi": 100 * ci.loc["dT", 1],
                     "b_P_pct_per_100pct": 100 * r.params["dP_rel"], "p_P": r.pvalues["dP_rel"],
                     "b_P_lo": 100 * ci.loc["dP_rel", 0], "b_P_hi": 100 * ci.loc["dP_rel", 1],
                     "R2": r.rsquared}) # parameters of the regression
        if verbose: # To retrieve the data
            t = rows[-1]
            print(f"{crop:<24} window {win:<8} n = {t['n']}  ({t['n_comarques']} comarques)\n"
                  f"  b_T = {t['b_T_pct_per_C']:+6.1f} % per degC       [{t['b_T_lo']:+.1f}, {t['b_T_hi']:+.1f}]  p = {t['p_T']:.3f}\n"
                  f"  b_P = {t['b_P_pct_per_100pct']:+6.1f} % per +100 % rain  [{t['b_P_lo']:+.1f}, {t['b_P_hi']:+.1f}]  p = {t['p_P']:.3f}\n"
                  f"  R2  = {t['R2']:.2f}")
        data.append(d.assign(crop_h=crop))
    return pd.DataFrame(rows), pd.concat(data, ignore_index=True)
