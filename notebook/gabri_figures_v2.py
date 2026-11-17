"""Paper figures, version 2 (Gabri). Run from notebook/: uv run --offline --project ../.. python gabri_figures_v2.py

Rebuilds four figures with the same data and methods as gabri_idea6/4/2.ipynb (cached raw data).
"""
from pathlib import Path

import holidays
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import opendata_bcn as bcn
import xema

OUT = Path("..") / "figures" / "Gabri"
plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.22,
    "legend.frameon": False,
})
# one colour per variable, used in every figure
C = {"hydro": "#1f77b4", "rain": "#17a2a2", "reservoir": "#6b4fa0", "imports": "#d62728",
     "gas": "#8c564b", "other": "#9e9e9e", "base": "#cfcfcf", "cold": "#3b75c4", "heat": "#e4572e",
     "olive": "#6b8e23", "dry": "#b5651d", "wet": "#2b7bba"}
DROUGHT = (pd.Timestamp("2022-01-01"), pd.Timestamp("2024-12-31"))


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200)
    fig.savefig(OUT / f"{name}.svg")
    plt.close(fig)


def note(fig, text):
    fig.text(0.01, 0.008, text, fontsize=6.5, ha="left", va="bottom", color="dimgrey")


# ---------------------------------------------------------------- 1. demand vs temperature
def hinge_fit(t, y, t_cold, t_hot):
    X = np.column_stack([np.ones(len(t)), np.clip(t_cold - t, 0, None), np.clip(t - t_hot, 0, None)])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef, ((y - X @ coef) ** 2).sum()


def fig_demand():
    t = xema.download_daily("X4", "1000", "2019-01-01", "2025-12-31").rename(columns={"value": "temp_c"})
    d = xema.download_demand("2019-01-01", "2025-12-31")
    df = d.merge(t, on="date", how="inner", validate="one_to_one")
    cat = holidays.Spain(subdiv="CT", years=range(2022, 2026))
    keep = ((df["date"] >= "2022-01-01") & (df["date"].dt.dayofweek < 5)
            & ~df["date"].dt.date.isin(cat.keys()) & (df["date"].dt.month != 8)
            & (df["date"] != "2025-04-28"))
    fit = df.loc[keep].assign(demand_gwh=lambda x: x["demand_mwh"] / 1000)
    assert len(fit) == 912, len(fit)  # known value from the paper
    tt, y = fit["temp_c"].to_numpy(), fit["demand_gwh"].to_numpy()
    best = min(((hinge_fit(tt, y, tc, th)[1], tc, th) for tc in np.arange(10, 20.5, 0.5)
                for th in np.arange(tc, 24.5, 0.5)))
    _, tc, th = best
    (base, a_c, a_h), _ = hinge_fit(tt, y, tc, th)

    g = np.linspace(tt.min(), tt.max(), 300)
    cold, heat = a_c * np.clip(tc - g, 0, None), a_h * np.clip(g - th, 0, None)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(g, 0, base, color=C["base"], lw=0, label=f"base load ({base:.0f} GWh/day)")
    ax.fill_between(g, base, base + cold, color=C["cold"], alpha=0.55, lw=0, label="extra for heating")
    ax.fill_between(g, base, base + heat, color=C["heat"], alpha=0.55, lw=0, label="extra for cooling")
    ax.scatter(tt, y, s=7, color="black", alpha=0.35, lw=0, label="one weekday (n = 912)")
    ax.plot(g, base + cold + heat, color="black", lw=1.6)
    ax.axvline(tc, color="dimgrey", lw=0.8, ls=":")
    ax.axvline(th, color="dimgrey", lw=0.8, ls=":")
    box = dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2)
    ax.annotate(f"+{a_c:.1f} GWh per °C\nbelow {tc:.0f} °C", xy=(8, base + a_c * (tc - 8)),
                xytext=(5.5, 60), color=C["cold"], fontweight="bold", bbox=box,
                arrowprops=dict(arrowstyle="->", color=C["cold"]))
    ax.annotate(f"+{a_h:.1f} GWh per °C\nabove {th:.0f} °C", xy=(29, base + a_h * (29 - th)),
                xytext=(26.5, 60), color=C["heat"], fontweight="bold", bbox=box, ha="center",
                arrowprops=dict(arrowstyle="->", color=C["heat"]))
    ax.text((tc + th) / 2, 30, "comfort\nzone", ha="center", fontsize=8, color="dimgrey")
    ax.set_ylim(0, 170)
    ax.set_xlabel("Mean daily temperature at Barcelona-Raval (°C)")
    ax.set_ylabel("Daily electricity demand in Catalonia (GWh)")
    ax.set_title("Each degree of heat costs more electricity than each degree of cold")
    ax.legend(loc="upper center", ncol=4, fontsize=7.5, bbox_to_anchor=(0.5, 1.0))
    note(fig, "Weekdays 2022-2025 without holidays, August and 28 Apr 2025. Two-threshold least-squares "
              "fit, thresholds on a 0.5 °C grid. Sources: Catalan open data, XEMA (X4).")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "idea6_demand_vs_temperature")
    print("demand:", len(fit), tc, th, round(a_c, 2), round(a_h, 2), round(base, 1))


# ---------------------------------------------------------------- 2. drought and replacement
def fig_drought():
    gen = xema.download_generation(2019, 2025)
    gen_p = gen.pivot(index="date", columns="technology", values="value_mwh") / 1000
    res = xema.download_reservoirs("2019-01-01", "2025-12-31")
    cap = (res["volume_hm3"] / (res["pct"] / 100)).groupby(res["reservoir"]).median()
    res = res.assign(capacity_hm3=res["reservoir"].map(cap))
    basin = res.groupby("date").agg(volume=("volume_hm3", "sum"), capacity=("capacity_hm3", "sum"))
    basin_m = (100 * basin["volume"] / basin["capacity"]).resample("MS").mean()

    pyr = ["Y4", "W5", "CJ", "CD", "CT", "DP", "YA", "WQ", "CP", "XQ", "YC", "XH", "YG"]
    rain = {}
    for st in pyr:
        dd = xema.download_daily(st, "1300", "2019-01-01", "2025-12-31").set_index("date")["value"]
        mm = dd.resample("MS").agg(["sum", "count"])
        rain[st] = mm["sum"].where(mm["count"] >= 25)
    rain_m = pd.DataFrame(rain).mean(axis=1)
    hydro = gen_p["Hidráulica"]

    groups = {"Hydro": ["Hidráulica"], "Combined cycle": ["Ciclo combinado"], "Nuclear": ["Nuclear"],
              "Wind": ["Eólica"], "Solar PV": ["Solar fotovoltaica"], "Cogeneration": ["Cogeneración"],
              "Other": ["Solar térmica", "Otras renovables", "Residuos no renovables", "Residuos renovables"]}
    annual = pd.DataFrame({k: gen_p[v].sum(axis=1).resample("YS").sum() for k, v in groups.items()})
    ind = xema.download_indicators("2019-01-01", "2025-12-31")
    annual["Net imports"] = ind.set_index("date")["net_imports_gwh"].resample("YS").sum()
    annual.index = annual.index.year
    step = annual.loc[2023] - annual.loc[2022]
    print("2023 vs 2022:", step.round(0).to_dict())

    fig = plt.figure(figsize=(10, 8.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.15], hspace=0.38)
    ax = fig.add_subplot(gs[0])
    series = {"Pyrenean rain (12-month total)": (rain_m.rolling(12).sum(), C["rain"], "-"),
              "Hydro generation (12-month total)": (hydro.rolling(12).sum(), C["hydro"], "-"),
              "Conques Internes reservoirs (volume)": (basin_m, C["reservoir"], "--")}
    for label, (s, col, ls) in series.items():
        s = s.dropna()
        ax.plot(s.index, 100 * s / s.mean(), color=col, lw=2.2, ls=ls, label=label)
    ax.axhline(100, color="black", lw=0.8)
    ax.axvspan(*DROUGHT, color=C["dry"], alpha=0.10, lw=0)
    ax.text(DROUGHT[0] + (DROUGHT[1] - DROUGHT[0]) / 2, 8, "2022-2024 drought", ha="center",
            color=C["dry"], fontweight="bold")
    low = basin_m.idxmin()
    ax.annotate(f"reservoirs at {basin_m.min():.0f}% of capacity\n({low:%b %Y})",
                xy=(low, 100 * basin_m.min() / basin_m.dropna().mean()), xytext=(pd.Timestamp("2024-09-01"), 30),
                fontsize=8, color=C["reservoir"], arrowprops=dict(arrowstyle="->", color=C["reservoir"]))
    ax.text(0.01, 0.04, "Annual correlation with hydro: Pyrenean rain r = 0.80, reservoirs r = 0.69",
            transform=ax.transAxes, fontsize=8, color="dimgrey")
    ax.set_ylim(0, 175)
    ax.set_ylabel("% of the 2019-2025 mean")
    ax.set_title("a  Hydropower follows Pyrenean rain more closely than the reservoirs near Barcelona")
    ax.legend(loc="upper left", ncol=3, fontsize=7.5)

    ax = fig.add_subplot(gs[1])
    names = list(step.index)
    cum = np.concatenate([[0], np.cumsum(step.to_numpy())])
    colors = [C["hydro"] if n == "Hydro" else C["imports"] if n == "Net imports"
              else C["gas"] if n == "Combined cycle" else C["other"] for n in names]
    ax.bar(names, step.to_numpy(), bottom=cum[:-1], color=colors, width=0.62)
    for i in range(len(names)):  # connectors between steps
        ax.plot([i + 0.31, i + 0.69], [cum[i + 1]] * 2, color="black", lw=0.6)
    ax.bar(len(names), cum[-1], color="black", width=0.62)
    for i, v in enumerate(step.to_numpy()):
        lo = min(cum[i], cum[i + 1])
        ax.text(i, lo - 90, f"{v:+,.0f}", ha="center", va="top", fontsize=8)
    ax.text(len(names), min(cum[-1], 0) - 90, f"{cum[-1]:+,.0f}", ha="center", va="top", fontsize=8)
    ax.set_ylim(-4400, 700)
    ax.set_xticks(range(len(names) + 1), names + ["Total supply"], rotation=0, fontsize=8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Change 2023 vs 2022 (GWh)")
    ax.annotate("imports replaced lost gas,\nnuclear and hydro output\n(≈13% of demand)",
                xy=(names.index("Net imports"), cum[-2] + step["Net imports"] / 2),
                xytext=(names.index("Net imports") - 2.6, cum[-2] + 900), fontsize=8, color=C["imports"],
                arrowprops=dict(arrowstyle="->", color=C["imports"]))
    ax.set_title("b  In 2023, the year of the deepest drought, the gap was filled by imports")
    ax.grid(axis="x", visible=False)
    note(fig, "Sources: REData (REE) monthly generation; XEMA daily rain, mean of 13 Pyrenean valley stations; "
              "ACA reservoirs (nine Conques Internes reservoirs); Catalan energy indicators (net imports = "
              "exchange balance).")
    fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.08)
    save(fig, "idea6_hydro_drought_replacement")


# ---------------------------------------------------------------- 3. olive oil
def fig_olive():
    cpi = xema.download_cpi().set_index("date")
    stations = ["VK", "VH", "WK", "UM", "D1", "WJ", "U7", "DB", "VQ", "DK"]
    cat = {}
    for st in stations:
        dd = xema.download_daily(st, "1300", "2002-01-01", "2025-12-31").set_index("date")["value"]
        mm = dd.resample("MS").agg(["sum", "count"])
        cat[st] = mm["sum"].where(mm["count"] >= 25)
    rain_cat = pd.DataFrame(cat).mean(axis=1)
    sites = {"jaen": (37.77, -3.79), "cordoba": (37.89, -4.78)}
    rain_and = pd.DataFrame({n: xema.download_rain_openmeteo(n, la, lo, "2002-01-01", "2025-12-31")
                             .set_index("date")["value"].resample("MS").sum()
                             for n, (la, lo) in sites.items()}).mean(axis=1)

    def hyd(r):
        return pd.Series({y: r.loc[f"{y - 1}-10-01":f"{y}-09-01"].sum() for y in range(2003, 2026)})

    an = pd.DataFrame({"and": hyd(rain_and), "cat": hyd(rain_cat)})
    an = (an - an.mean()) / an.std()
    an["price"] = [cpi.loc[f"{y}-12-01", "olive_oil_yoy"] for y in an.index]
    driest = sorted(an["and"].nsmallest(4).index)
    print("driest Andalusia:", driest)

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], hspace=0.38, wspace=0.18)
    ax = fig.add_subplot(gs[0, :])
    s = cpi["olive_oil_yoy"].dropna().loc["2003":]
    for y in driest:  # hydrological year of each of the four driest years
        ax.axvspan(pd.Timestamp(f"{y - 1}-10-01"), pd.Timestamp(f"{y}-09-30"), color=C["dry"], alpha=0.16, lw=0)
        ax.text(pd.Timestamp(f"{y - 1}-10-01") + pd.Timedelta(days=182), -42, str(y), ha="center",
                color=C["dry"], fontsize=8, fontweight="bold")
    ax.fill_between(s.index, 0, s, where=s > 0, color=C["olive"], alpha=0.25, lw=0)
    ax.plot(s.index, s, color=C["olive"], lw=1.8, label="olive oil")
    ax.plot(cpi["general_yoy"].loc["2003":], color="black", lw=1, label="all consumer prices")
    ax.axhline(0, color="black", lw=0.6)
    pk = s.idxmax()
    ax.annotate(f"+{s.max():.1f}% ({pk:%b %Y})", xy=(pk, s.max()), xytext=(pk - pd.Timedelta(days=1700), 70),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", color="dimgrey"))
    ax.set_ylim(-50, 85)
    ax.set_ylabel("Annual price change (%)")
    ax.set_title("a  Olive oil prices jumped after three of the four driest years in Andalusia")
    ax.legend(loc="upper left", fontsize=8)

    for j, (key, region) in enumerate((("and", "Andalusia"), ("cat", "Catalonia"))):
        ax = fig.add_subplot(gs[1, j], sharey=None)
        x, yv = an[key], an["price"]
        r, p = stats.pearsonr(x, yv)
        rs, ps = stats.spearmanr(x, yv)
        ax.axvspan(-3, 0, color=C["dry"], alpha=0.07, lw=0)
        ax.scatter(x, yv, s=26, color=np.where(x < 0, C["dry"], C["wet"]), edgecolor="white", lw=0.5, zorder=3)
        b, a = np.polyfit(x, yv, 1)
        xs = np.array([-2.6, 2.6])
        ax.plot(xs, a + b * xs, color="black", lw=1)
        for yr in an.index:
            if yr in driest or abs(yv[yr]) > 30 or abs(x[yr]) > 1.6:
                ax.annotate(str(yr), (x[yr], yv[yr]), xytext=(4, 3), textcoords="offset points", fontsize=7)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_xlim(-2.6, 2.6)
        ax.set_ylim(-45, 70)
        ax.set_xlabel(f"Rain anomaly, {region} (z-score; < 0 = drier)")
        if j == 0:
            ax.set_ylabel("Olive oil price change in December (%)")
        ax.set_title(f"{'bc'[j]}  {region}\nr = {r:.2f} (p = {p:.3f}); Spearman {rs:.2f} (p = {ps:.3f})",
                     fontsize=9)
    note(fig, "Shaded bands: hydrological years (Oct-Sep) of the four driest years in Andalusia, 2003-2025. Each "
              "point is one year (n = 23). Sources: INE CPI (table 50905); Open-Meteo reanalysis; XEMA.")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.1)
    save(fig, "idea4_olive_timeline")


# ---------------------------------------------------------------- 4. shelters
def weighted_decile(income, weight):
    order = np.argsort(income.to_numpy())
    w = weight.to_numpy()[order]
    mid = (np.cumsum(w) - w / 2) / w.sum()
    dec = np.empty(len(income), dtype=int)
    dec[order] = np.minimum((mid * 10).astype(int) + 1, 10)
    return dec


def fig_shelters():
    sec = (bcn.download_sections()
           .merge(bcn.download_income(2023)[["section_id", "income_eur"]], on="section_id", validate="one_to_one")
           .merge(bcn.download_population(2024), on="section_id", validate="one_to_one"))
    shelters = bcn.download_shelters()
    sec["decile"] = weighted_decile(sec["income_eur"], sec["population"])
    for r in (400, 800):
        zone = shelters.buffer(r).union_all()
        sec[f"pop_{r}"] = sec["population"] * sec.geometry.intersection(zone).area / sec.geometry.area
    by = sec.groupby("decile").agg(pop=("population", "sum"), p400=("pop_400", "sum"),
                                   p800=("pop_800", "sum"), inc=("income_eur", "median"))
    by = by.assign(pct_400=100 * by["p400"] / by["pop"], pct_800=100 * by["p800"] / by["pop"])
    city = {r: 100 * sec[f"pop_{r}"].sum() / sec["population"].sum() for r in (400, 800)}
    print("shelters:", len(sec), len(shelters), {k: round(v, 1) for k, v in city.items()},
          by[["pct_400", "pct_800"]].round(1).loc[[1, 10]].to_dict())

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = by.index.to_numpy()
    ax.bar(x, by["pct_800"], color=C["wet"], alpha=0.30, width=0.7, label="within 800 m (about 10 min)")
    ax.bar(x, by["pct_400"], color=C["wet"], width=0.42, label="within 400 m (about 5 min)")
    ax.axhline(99, color=C["imports"], lw=1.4, ls="--")
    ax.text(0.45, 101.5, "City Council: 99% of residents have a shelter within 10 minutes", fontsize=8,
            color=C["imports"], va="bottom")
    for d in (1, 10):
        ax.text(d, by.loc[d, "pct_400"] / 2, f"{by.loc[d, 'pct_400']:.1f}%", ha="center", color="white",
                fontsize=8, fontweight="bold", rotation=90)
    ax.set_xticks(x, [f"{d}\n{by.loc[d, 'inc'] / 1000:.0f}k" for d in x])
    ax.set_xlabel("Income decile (1 = poorest), with median income per person (EUR)")
    ax.set_ylabel("Residents with a shelter nearby (%)")
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 101, 20))
    ax.grid(axis="x", visible=False)
    ax.set_title("Almost every Barcelona resident lives near a climate shelter, rich or poor")
    ax.legend(loc="lower left", ncol=2, fontsize=8, facecolor="white", framealpha=0.9, frameon=True)
    note(fig, f"City-wide: {city[400]:.1f}% within 400 m, {city[800]:.1f}% within 800 m. Straight-line distance; "
              "population (1 Jan 2024) assumed uniform inside each census section. Source: Open Data BCN.")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "idea2_accessibility_by_income")


if __name__ == "__main__":
    fig_demand()
    fig_drought()
    fig_olive()
    fig_shelters()
