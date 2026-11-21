"""Figures for the crop-climate results. We've figured that the plots may be better in an
aside script as there are many types and some of them are trial and error to see wether
they fit better in the presentation or the paper.
Plots:
fig_time(data, crop)      rain anomaly and yield anomaly by year, two stacked panels
fig_scatter(data, crop)   yield anomaly vs rain anomaly, comarca x year, drought years highlighted
fig_maps(geo, data, cm, crop)   map located rain anomally and map located yield anomaly.
Every function shows its figure itself (once), saves nothing to disk, and returns None.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import statsmodels.formula.api as smf # type: ignore

# Color parameters and names of studied crops
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#a8a7a2"   # categorical slots 1, 2, 3 + neutral gray
NAMES = {"Blat": "Wheat", "Ordi": "Barley", "Blat de moro": "Maize", "Ametller": "Almond",
         "Olivera": "Olive", "Vinya de raïm per a vi": "Vine"}


def _style(ax, grid="y"):
    """This function homogenizes the axis and grid format so we don't have to specify it in every cell."""
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
    """ This function plots the window of the crop ('Oct-Jun', window name) from climate_yield.CROP_WINDOW,
    which can be used either for labels and for code itself (through `w`)"""
    import hug_climate_yield as C
    w = C.CROP_WINDOW.get(crop, "cereal")
    m0, m1, _ = C.WINDOWS[w]
    return f"{_MES[m0]}–{_MES[m1]}", w


def _done(f):
    """This figure is simply showing the plot after the main function is called and then it closes without saving 
    anything. Nothing is written to disk. Returns None, so a figure call can sit anywhere in a cell, several per 
    cell, with no duplicates. Used at the end of all cells"""
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

def _save(f, path, dpi=300):
    """Writes the figure to `path` (format from the extension: png, pdf, svg...). Creates the folder if needed. 
    (did it manually though)"""
    import os
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    f.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=f.get_facecolor())

def _fig(*a, **k):
    """This function is, once more, a plot helper to avoid repeating in each function (for pannels)"""
    f, ax = plt.subplots(*a, **k)
    f.patch.set_facecolor(SURF)
    return f, ax


def fig_time(data, crop="Blat", mark=(2008, 2015, 2020, 2023), show_value=False):
    """This function builds a pannel with the rainfall anomaly (upper) and the yield anomaly (down) in a time series """
    d = data[data.crop_h == crop].groupby("year")[["e", "dP_rel"]].mean() * 100 # Data is obtained
    f, (a1, a2) = _fig(2, 1, figsize=(8, 5.6), sharex=True, gridspec_kw={"hspace": 0.18})
    for ax, col, ttl in ((a1, "dP_rel", f"Season rainfall ({_win(crop)[0]}), relative to the mean"), # Building of the 2 plots
                         (a2, "e", f"{NAMES.get(crop, crop)} yield, relative to its trend")):
        v = d[col]
        ax.bar(d.index, v, width=0.7, color=np.where(v >= 0, BLUE, ORANGE))
        ax.axhline(0, color=INK2, lw=1)
        #ax.set_title(ttl, loc="left", fontsize=11, color=INK)
        if ax == a1:
            ax.set_ylabel("Rainfall anomaly (%)")
        else:
            ax.set_ylabel("Yield anomaly (%)")
        ax.margins(y=0.25) # we make room for the year labels
        _style(ax)
        for y in mark: # we label only the years we have found that were specially dry or wet
            if y in v.index:
                txt = f"{y}\n{v[y]:+.0f}%" if show_value else str(y)
                dy = 4 if v[y] >= 0 else (-22 if show_value else -11)
                ax.annotate(txt, (y, v[y]), xytext=(0, dy),
                            textcoords="offset points", ha="center", fontsize=9, color=INK)
    a2.set_xticks(d.index[::2])
    #f.legend([Patch(color=BLUE), Patch(color=ORANGE)], ["above normal", "below normal"],
    #         frameon=False, fontsize=9, labelcolor=INK2, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.02))
    return _done(f)


def fig_scatter(data, crop="Blat", highlight=(2023, 2015, 2020)):
    """This function plots a scatter of points (one per year and region) highlighting certain years only, in a % yield and 
    % rain plot (the anomalies from respect their means), while plotting a regression to determine the dependency of the anomalies
    and to compare it to `e`."""
    d = data[data.crop_h == crop]
    r = smf.ols("e ~ dT + dP_rel", d).fit()
    f, ax = _fig(figsize=(7, 5))
    highlight = tuple(highlight)[:3] # three highlighted years + grey the rest
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
    #ax.set_title(f"{NAMES.get(crop, crop)}: wetter seasons go with bigger harvests",
    #             loc="left", fontsize=12, color=INK, pad=20)
    #ax.text(0, 1.015, "Each dot = one county in one year", transform=ax.transAxes,
    #        fontsize=9, color=INK2, va="bottom")
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="upper left")
    _style(ax, "both")
    return _done(f)




def load_comarques(path, fix_comarca, name_col=None, known=None):
    """This function reads the comarca boundaries (GeoJSON/shapefile given by the teacher) and puts the names in the same spelling
    as the crop table."""
    import geopandas as gpd
    g = gpd.read_file(path)
    if name_col is None:# column whose values match known names best
        known = set(known) if known is not None else set()
        score = {c: sum(fix_comarca(v) in known for v in g[c].astype(str)) for c in g.columns if c != "geometry"}
        name_col = max(score, key=score.get) if known else next(c for c in g.columns if g[c].dtype == object)
        print("name column:", name_col, "| matches:", score.get(name_col))
    g = g.assign(comarca=g[name_col].astype(str).map(fix_comarca))
    return g.to_crs(4326)[["comarca", "geometry"]]


def fig_maps(geo, data, cm, years=(2015, 2020, 2023), crop="Blat", window=None):
    """This function creates a pannel which compares rain anomaly to yield anomaly per region for a preselected years. Top row: rain anomaly, 
    bottom row: yield anomaly. One shared colour scale per row (so the years can be compared). Hatched regions = no data for that comarca/year."""
    import hug_climate_yield as C # Data is imported from the other script
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    from matplotlib.cm import ScalarMappable
    window = window or _win(crop)[1] # month window that belongs to the crop
    rain = C.seasonal(cm, window).assign(v=lambda d: d.dP_rel * 100) # assign the rain to regions
    yld = data[data.crop_h == crop].assign(v=lambda d: d.e * 100) # the yield as well
    cmap = LinearSegmentedColormap.from_list("div", [ORANGE, "#f1f0ec", BLUE]) # and prepare the colorscale in the map
    rows = [(rain, f"Rainfall ({_win(crop)[0]})", "% of the mean"),
            (yld, f"{NAMES.get(crop, crop)} yield", "% of its trend")]
    f, axs = plt.subplots(2, len(years), figsize=(3.2 * len(years) + 1.2, 5.6), squeeze=False,
                          gridspec_kw={"hspace": 0.0, "wspace": 0.0})
    f.patch.set_facecolor(SURF)
    for i, (tab, title, unit) in enumerate(rows):
        sub = tab[tab.year.isin(years)]
        lim = float(np.ceil(np.nanpercentile(sub.v.abs(), 98) / 5) * 5) or 5 # symmetric around 0
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


def fig_quadrants(data, crop="Blat", highlight=(2023, 2015, 2020), bins=8, min_n=3):
    """This function plots rainfall anomaly (x) vs temperature anomaly (y). Each cell is coloured by the average yield anomaly of the county-years 
    that fall in it (blue = above trend, orange = below). Cells with fewer than min_n are blank."""
    import matplotlib.patheffects as pe
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    d = data[data.crop_h == crop].dropna(subset=["dP_rel", "dT", "e"])
    x, y, e = d.dP_rel.to_numpy() * 100, d.dT.to_numpy(), d.e.to_numpy() * 100
    lx, ly = np.abs(x).max() * 1.02, np.abs(y).max() * 1.02
    rng = [[-lx, lx], [-ly, ly]]
    n, xe, ye = np.histogram2d(x, y, bins=bins, range=rng) # we prepare the grids and the average per square
    tot = np.histogram2d(x, y, bins=bins, range=rng, weights=e)[0]
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = np.where(n >= min_n, tot / n, np.nan)
    v = np.nanmax(np.abs(mean))
    cmap = LinearSegmentedColormap.from_list("ob", [ORANGE, "#efeee9", BLUE]) # color scaling
    f, ax = _fig(figsize=(6.6, 5.2))
    im = ax.pcolormesh(xe, ye, np.ma.masked_invalid(mean.T), cmap=cmap, norm=TwoSlopeNorm(0, -v, v),
                       edgecolor=SURF, linewidth=1.5) # we apply the colour
    ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
    halo = [pe.withStroke(linewidth=3, foreground=SURF)]
    for i, yr in enumerate(tuple(highlight)[:3]):
        g = d[d.year == yr] # one marker per year: mean of all counties
        px, py = g.dP_rel.mean() * 100, g.dT.mean()
        ax.scatter(px, py, s=80, color="#ffffff", edgecolor=INK, linewidth=1.4, zorder=4)
        ax.annotate(str(yr), (px, py), xytext=(-9, -15) if i == 1 else (9, 6), textcoords="offset points",
                    ha="right" if i == 1 else "left", fontsize=10, color=INK, fontweight="bold",
                    path_effects=halo, zorder=5) # 2nd label goes below-left so close years do not overlap
    ax.set_xlabel("Rainfall vs normal (%)", fontsize=10); ax.set_ylabel("Temperature vs normal (°C)", fontsize=10)
    ax.set_title(NAMES.get(crop, crop), loc="left", fontsize=13, fontweight="bold", color=INK, pad=10)
    cb = f.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_label("Yield vs trend (%)", fontsize=10, color=INK2)
    cb.outline.set_visible(False); cb.ax.tick_params(colors=INK2, length=0, labelsize=9)
    _style(ax, "x"); ax.grid(False)
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    return _done(f)


def fig_scatter_grid(data, crop="Blat", highlight=(2023, 2015, 2020), bins=14, min_n=2, color="dT"):
    """This function uses the same strategy as for scatter but with a heatmap, therefore as quadrants. Plots yield anomaly vs rainfall anomaly, 
    drawn as squares. color="dT": average temperature anomaly in each square (orange = warmer, blue = cooler); color="count": number of county-years 
    (blue scale). More or less same procedure"""
    import matplotlib.patheffects as pe
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, Normalize
    d = data[data.crop_h == crop].dropna(subset=["dP_rel", "dT", "e"])
    x, y = d.dP_rel.to_numpy() * 100, d.e.to_numpy() * 100
    lx, ly = np.abs(x).max() * 1.02, np.abs(y).max() * 1.02
    rng = [[-lx, lx], [-ly, ly]]
    n, xe, ye = np.histogram2d(x, y, bins=bins, range=rng)
    if color == "count":
        val = np.where(n >= min_n, n, np.nan)
        cmap, norm, lab = (LinearSegmentedColormap.from_list("c", ["#e3edfa", BLUE, "#143f7a"]),
                           Normalize(1, np.nanmax(val)), "County-years per square")
    else:
        tot = np.histogram2d(x, y, bins=bins, range=rng, weights=d.dT.to_numpy())[0]
        with np.errstate(invalid="ignore", divide="ignore"):
            val = np.where(n >= min_n, tot / n, np.nan)
        v = np.nanmax(np.abs(val))
        cmap, norm, lab = (LinearSegmentedColormap.from_list("bo", [BLUE, "#efeee9", ORANGE]),
                           TwoSlopeNorm(0, -v, v), "Temperature vs normal (°C)")
    f, ax = _fig(figsize=(6.6, 5.2))
    im = ax.pcolormesh(xe, ye, np.ma.masked_invalid(val.T), cmap=cmap, norm=norm, edgecolor=SURF, linewidth=1.5)
    ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
    halo = [pe.withStroke(linewidth=3, foreground=SURF)]
    for i, yr in enumerate(tuple(highlight)[:3]):
        g = d[d.year == yr]                                   # one marker per year: mean of all counties
        px, py = g.dP_rel.mean() * 100, g.e.mean() * 100
        ax.scatter(px, py, s=80, color="#ffffff", edgecolor=INK, linewidth=1.4, zorder=4)
        ax.annotate(str(yr), (px, py), xytext=(-9, -15) if i == 1 else (9, 6), textcoords="offset points",
                    ha="right" if i == 1 else "left", fontsize=10, color=INK, fontweight="bold",
                    path_effects=halo, zorder=5)       # 2nd label goes below-left so close years do not overlap
    ax.set_xlabel("Rainfall vs normal (%)", fontsize=10); ax.set_ylabel("Yield vs trend (%)", fontsize=10)
    ax.set_title(NAMES.get(crop, crop), loc="left", fontsize=13, fontweight="bold", color=INK, pad=10)
    cb = f.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_label(lab, fontsize=10, color=INK2)
    cb.outline.set_visible(False); cb.ax.tick_params(colors=INK2, length=0, labelsize=9)
    _style(ax, "x"); ax.grid(False)
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    return _done(f)


def fig_scatter_panel(data, crops=("Blat", "Ordi", "Olivera", "Blat de moro"), highlight=(2023, 2015, 2020), save=None, dpi=300):
    """This function repeats the scatter function but to build a pannel 2x2: yield anomaly vs rainfall anomaly, one crop per panel. 
    Each panel has its own axes."""
    crops = tuple(crops)[:4]
    f, axs = _fig(2, 2, figsize=(10, 7.4), gridspec_kw={"hspace": 0.38, "wspace": 0.2})
    highlight = tuple(highlight)[:3]
    style = list(zip(highlight, (ORANGE, AQUA, BLUE), ("o", "s", "^")))
    for ax, crop in zip(axs.ravel(), crops):
        d = data[data.crop_h == crop]
        if d.empty:
            ax.set_visible(False)
            continue
        r = smf.ols("e ~ dT + dP_rel", d).fit()
        h = d.year.isin(highlight)
        ax.scatter(d.dP_rel[~h] * 100, d.e[~h] * 100, s=12, color=GREY, alpha=0.5, lw=0)
        for y, col, mk in style:
            g = d[d.year == y]
            ax.scatter(g.dP_rel * 100, g.e * 100, s=28, color=col, marker=mk, lw=0)
        x = np.linspace(d.dP_rel.min(), d.dP_rel.max(), 50)
        ax.plot(x * 100, 100 * (r.params["Intercept"] + r.params["dP_rel"] * x), color=INK, lw=1.8)
        ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
        ax.text(0.98, 0.04, f"$\\beta_R$ = {r.params['dP_rel']:+.2f}   "
                            f"$R^2$ = {r.rsquared:.2f}",
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK2,
                bbox=dict(boxstyle="round,pad=0.35", fc=SURF, ec="none", alpha=0.85))
        ax.set_title(NAMES.get(crop, crop), loc="left", fontsize=12, fontweight="bold", color=INK)
        ax.set_xlabel(f"Rainfall vs normal, {_win(crop)[0]} (%)", fontsize=9)
        ax.set_ylabel("Yield vs trend (%)", fontsize=9)
        _style(ax, "both")
    handles = [plt.Line2D([], [], marker="o", ls="", color=GREY, markersize=5, label="other years")]
    handles += [plt.Line2D([], [], marker=mk, ls="", color=col, markersize=6, label=str(y)) for y, col, mk in style]
    f.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=10, labelcolor=INK2,
             bbox_to_anchor=(0.5, -0.01))
    f.subplots_adjust(top=0.94, bottom=0.12, left=0.07, right=0.98)
    if save:
        _save(f, save, dpi)
    return _done(f)


def fig_maps_panel(geo, data, cm, years=(2015, 2020, 2023), crops=("Blat", "Ordi", "Olivera", "Blat de moro"),
                   rain_window=None, pct=98, save=None, dpi=300):
    """This function repeats the map function but now as a pannel. Collumn show years, each row is either the rain anomaly of one specific time 
    window or the yield anomaly for a crop in the same time window as the first rain anomaly row right avobe it"""
    import hug_climate_yield as C
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    from matplotlib.cm import ScalarMappable
    crops, years = tuple(crops), tuple(years)
    groups = {}
    for c in crops: # We group the grops by rain window
        groups.setdefault(rain_window or C.CROP_WINDOW[c], []).append(c)
    rain = {w: C.seasonal(cm, w).assign(v=lambda d: d.dP_rel * 100) for w in groups} # we build the two tables having in common same scale colour
    yld = {c: data[data.crop_h == c].assign(v=lambda d: d.e * 100) for c in crops}

    def make_norm(tabs):
        """This helper function takes the abs value of all plotted years and 98th percentile, to fix the color scale for all crop subplots"""
        v = np.concatenate([t[t.year.isin(years)].v.dropna().abs().to_numpy() for t in tabs])
        p = float(np.nanpercentile(v, pct))
        step = 5 if p >= 10 else 1
        lim = float(np.ceil(p / step) * step) or step # symmetric around 0
        return TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim)
    n_rain, n_yld = make_norm(list(rain.values())), make_norm(list(yld.values()))
    cmap = LinearSegmentedColormap.from_list("div", [ORANGE, "#f1f0ec", BLUE])

    slots = [] # (kind, key) per grid row
    for k, (w, cs) in enumerate(groups.items()): # we manage the row layout
        if k:
            slots.append(("gap", None))
        slots.append(("rain", w))
        slots += [("crop", c) for c in cs]
    nc, nrows = len(years), sum(k != "gap" for k, _ in slots)
    f = plt.figure(figsize=(2.5 * nc + 1.0, 1.75 * nrows + 0.3 * (len(groups) - 1) + 1.0)) 
    f.patch.set_facecolor(SURF)
    gs = f.add_gridspec(len(slots), nc, height_ratios=[0.18 if k == "gap" else 1 for k, _ in slots],
                        left=0.09, right=0.99, top=0.95, bottom=0.10, hspace=0.0, wspace=0.0)
    first = True
    for r, (kind, key) in enumerate(slots): # now with all slots of the pannel, we assign the anomalies, colours and positions 
        if kind == "gap":
            continue
        tab = rain[key] if kind == "rain" else yld[key]
        norm = n_rain if kind == "rain" else n_yld
        label = f"Rainfall {_MES[C.WINDOWS[key][0]]}–{_MES[C.WINDOWS[key][1]]}" if kind == "rain" else NAMES.get(key, key)
        for j, y in enumerate(years):
            ax = f.add_subplot(gs[r, j])
            m = geo.merge(tab[tab.year == y][["comarca", "v"]], on="comarca", how="left")
            if m.v.isna().any():
                m[m.v.isna()].plot(ax=ax, color="#ebeae6", edgecolor=SURF, lw=0.4, hatch="////")
            if m.v.notna().any():
                m[m.v.notna()].plot(ax=ax, column="v", cmap=cmap, norm=norm, edgecolor=SURF, lw=0.4)
            ax.set_axis_off(); ax.set_aspect("equal")
            if first:
                ax.set_title(str(y), fontsize=12, fontweight="bold", color=INK)
            if j == 0:
                ax.text(-0.02, 0.5, label, transform=ax.transAxes, rotation=90, ha="right", va="center",
                        fontsize=10.5 if kind == "rain" else 10, fontweight="bold" if kind == "rain" else "normal",
                        color=INK if kind == "rain" else INK2)
        first = False
    for x0, norm, lab in ((0.10, n_rain, "Rainfall vs normal (%)"), (0.58, n_yld, "Yield vs trend (%)")):
        cb = f.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=f.add_axes([x0, 0.055, 0.30, 0.012]),
                        orientation="horizontal")
        cb.set_label(lab, color=INK2, fontsize=9); cb.ax.tick_params(colors=INK2, length=0, labelsize=8)
        cb.outline.set_visible(False)
    f.text(0.01, 0.005, "Hatched = no data", fontsize=9, color=INK2)
    if save:
        _save(f, save, dpi)
    return _done(f)
