"""Figures for the crop-climate results (matplotlib, light theme).
fig_time(data, crop)      rain anomaly and yield anomaly by year, two stacked panels
fig_scatter(data, crop)   yield anomaly vs rain anomaly, comarca x year, drought years highlighted
`data` and `tab` are the two objects returned by climate_yield.fit(ya, cm).
Every function shows its figure itself (once), saves nothing to disk, and returns None.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import statsmodels.formula.api as smf # type: ignore

INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#a8a7a2"   # categorical slots 1, 2, 3 + neutral gray
NAMES = {"Blat": "Wheat", "Ordi": "Barley", "Blat de moro": "Maize", "Ametller": "Almond",
         "Olivera": "Olive", "Vinya de raïm per a vi": "Vine"}


def _style(ax, grid="y"):
    ax.set_facecolor(SURF)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, length=0)
    ax.grid(axis=grid, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(INK2); ax.yaxis.label.set_color(INK2)


_MES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _win(crop):
    """('Oct–Jun', window name) for a crop, from climate_yield.CROP_WINDOW."""
    import hug_climate_yield as C
    w = C.CROP_WINDOW.get(crop, "cereal")
    m0, m1, _ = C.WINDOWS[w]
    return f"{_MES[m0]}–{_MES[m1]}", w


def _done(f):
    """Shows the figure exactly once (notebook or script) and closes it. Nothing is written to disk.
    Returns None, so a figure call can sit anywhere in a cell, several per cell, with no duplicates."""
    try:
        from IPython import get_ipython
        from IPython.display import display
        if get_ipython() is not None:
            display(f)
            plt.close(f)
            return None
    except ImportError:
        pass
    plt.show()
    plt.close(f)


def _fig(*a, **k):
    f, ax = plt.subplots(*a, **k)
    f.patch.set_facecolor(SURF)
    return f, ax


def fig_time(data, crop="Blat", mark=(2008, 2015, 2020, 2023), show_value=False):
    d = data[data.crop_h == crop].groupby("year")[["e", "dP_rel"]].mean() * 100
    f, (a1, a2) = _fig(2, 1, figsize=(8, 5.6), sharex=True, gridspec_kw={"hspace": 0.18})
    for ax, col, ttl in ((a1, "dP_rel", f"Season rainfall ({_win(crop)[0]}), relative to the mean"),
                         (a2, "e", f"{NAMES.get(crop, crop)} yield, relative to its trend")):
        v = d[col]
        ax.bar(d.index, v, width=0.7, color=np.where(v >= 0, BLUE, ORANGE))
        ax.axhline(0, color=INK2, lw=1)
        ax.set_title(ttl, loc="left", fontsize=11, color=INK)
        ax.set_ylabel("%")
        ax.margins(y=0.25)                                       # room for the year labels
        _style(ax)
        for y in mark:                                           # label only the years we talk about
            if y in v.index:
                txt = f"{y}\n{v[y]:+.0f}%" if show_value else str(y)
                dy = 4 if v[y] >= 0 else (-22 if show_value else -11)
                ax.annotate(txt, (y, v[y]), xytext=(0, dy),
                            textcoords="offset points", ha="center", fontsize=9, color=INK)
    a2.set_xticks(d.index[::2])
    f.legend([Patch(color=BLUE), Patch(color=ORANGE)], ["above normal", "below normal"],
             frameon=False, fontsize=9, labelcolor=INK2, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.02))
    return _done(f)


def fig_scatter(data, crop="Blat", highlight=(2023, 2015, 2020)):
    d = data[data.crop_h == crop]
    r = smf.ols("e ~ dT + dP_rel", d).fit()
    f, ax = _fig(figsize=(7, 5))
    highlight = tuple(highlight)[:3]                      # three highlighted years + grey is the readable limit
    h = d.year.isin(highlight)
    ax.scatter(d.dP_rel[~h] * 100, d.e[~h] * 100, s=14, color=GREY, alpha=0.55, lw=0, label="other years")
    for y, col, mk in zip(highlight, (ORANGE, AQUA, BLUE), ("o", "s", "^")):
        g = d[d.year == y]
        ax.scatter(g.dP_rel * 100, g.e * 100, s=34, color=col, marker=mk, lw=0, label=str(y))
    x = np.linspace(d.dP_rel.min(), d.dP_rel.max(), 50)
    ax.plot(x * 100, 100 * (r.params["Intercept"] + r.params["dP_rel"] * x), color=INK, lw=2)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.text(0.98, 0.04, f"Slope $\\beta_R$ = {r.params['dP_rel']:.2f}\nModel $R^2$ = {r.rsquared:.2f}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color=INK2, linespacing=1.5)
    ax.set_xlabel(f"Rainfall anomaly {_win(crop)[0]} (% of the mean)")
    ax.set_ylabel("Yield anomaly (%)")
    ax.set_title(f"{NAMES.get(crop, crop)}: wetter seasons go with bigger harvests",
                 loc="left", fontsize=12, color=INK, pad=20)
    ax.text(0, 1.015, "Each dot = one county in one year", transform=ax.transAxes,
            fontsize=9, color=INK2, va="bottom")
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="upper left")
    _style(ax, "both")
    return _done(f)




def load_comarques(path, fix_comarca, name_col=None, known=None):
    """Reads the comarca boundaries (GeoJSON/shapefile) and puts the names in the same spelling
    as the crop table. name_col is detected automatically if not given."""
    import geopandas as gpd
    g = gpd.read_file(path)
    if name_col is None:                                    # column whose values match known names best
        known = set(known) if known is not None else set()
        score = {c: sum(fix_comarca(v) in known for v in g[c].astype(str)) for c in g.columns if c != "geometry"}
        name_col = max(score, key=score.get) if known else next(c for c in g.columns if g[c].dtype == object)
        print("name column:", name_col, "| matches:", score.get(name_col))
    g = g.assign(comarca=g[name_col].astype(str).map(fix_comarca))
    return g.to_crs(4326)[["comarca", "geometry"]]


def fig_maps(geo, data, cm, years=(2015, 2020, 2023), crop="Blat", window=None):
    """Top row: rain anomaly, bottom row: yield anomaly. One column per year, one shared colour
    scale per row (so the years can be compared). Hatched = no data for that comarca/year."""
    import hug_climate_yield as C
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    from matplotlib.cm import ScalarMappable
    window = window or _win(crop)[1]                      # month window that belongs to the crop
    rain = C.seasonal(cm, window).assign(v=lambda d: d.dP_rel * 100)
    yld = data[data.crop_h == crop].assign(v=lambda d: d.e * 100)
    cmap = LinearSegmentedColormap.from_list("div", [ORANGE, "#f1f0ec", BLUE])
    rows = [(rain, f"Rainfall ({_win(crop)[0]})", "% of the mean"),
            (yld, f"{NAMES.get(crop, crop)} yield", "% of its trend")]
    f, axs = plt.subplots(2, len(years), figsize=(3.2 * len(years) + 1.2, 5.6), squeeze=False,
                          gridspec_kw={"hspace": 0.0, "wspace": 0.0})
    f.patch.set_facecolor(SURF)
    for i, (tab, title, unit) in enumerate(rows):
        sub = tab[tab.year.isin(years)]
        lim = float(np.ceil(np.nanpercentile(sub.v.abs(), 98) / 5) * 5) or 5      # symmetric around 0
        norm = TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim)
        for j, y in enumerate(years):
            ax = axs[i, j]
            m = geo.merge(tab[tab.year == y][["comarca", "v"]], on="comarca", how="left")
            m[m.v.isna()].plot(ax=ax, color="#ebeae6", edgecolor=SURF, lw=0.4, hatch="////")
            m[m.v.notna()].plot(ax=ax, column="v", cmap=cmap, norm=norm, edgecolor=SURF, lw=0.4)
            ax.set_axis_off(); ax.set_aspect("equal")
            if i == 0:
                ax.set_title(str(y), fontsize=12, color=INK)
        axs[i, 0].text(-0.02, 0.5, title, transform=axs[i, 0].transAxes, rotation=90, ha="right",
                       va="center", fontsize=11, color=INK)
        cb = f.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=list(axs[i]), shrink=0.7, pad=0.02)
        cb.set_label(unit, color=INK2, fontsize=9); cb.ax.tick_params(colors=INK2, length=0); cb.outline.set_visible(False)
    f.text(0.01, 0.0, "Hatched = no data (too little area of this crop in the comarca, or no weather station).",
           fontsize=9, color=INK2)
    return _done(f)