# Figures

All figures are saved in the `Gabri/` folder (PNG at 200 dpi and SVG). The code is in the notebooks `notebook/gabri_heat_energy_demand.ipynb`, `notebook/gabri_drought_hydro_energy.ipynb` and `notebook/gabri_drought_olive_oil.ipynb`. The paper figures `hydro_drought_replacement`, `olive_oil_timeline` and `idea2_accessibility_by_income` are produced by `notebook/gabri_figures_v2.py` (same data and methods, redesigned layout; run from `notebook/`), which overwrites the notebook versions of the first and third. All `energy_demand_*` figures come from `notebook/gabri_idea6.ipynb`. Colours of the demand figures are colour-blind safe (Okabe-Ito, coolwarm, cividis).

## energy_demand_vs_temperature (.png, .svg)

Daily electricity demand in Catalonia against mean daily temperature, with a two-threshold piecewise linear fit, coloured (and marked) by season. Demand is shown as % above a mild day: 0% = 114 GWh, the fitted base load in the comfort zone.

- **Data:** demand from the Catalan open data dataset `hx6q-ykhb` (daily total, MWh, converted to GWh); temperature from XEMA daily data (`7bvh-jvq2`, variable 1000) at station X4, Barcelona - el Raval. Code in `notebook/gabri_heat_energy_demand.ipynb` and `notebook/xema.py`.
- **Sample:** weekdays 2022-2025 (912 days), excluding Catalan public holidays, August (holiday effect) and 28 Apr 2025 (Iberian blackout, 69 GWh).
- **First reading:** comfort zone between 17 and 22 °C (about 114 GWh/day). Demand rises about 2.9 GWh (2.5%) per °C below 17 °C and about 4.2 GWh (3.7%) per °C above 22 °C, so heat weighs more than cold. At the same temperature winter days consume more than spring days, so temperature explains only part of the variation (residual RMSE about 5.8 GWh).
- **Choice of station:** Raval is urban (33 m), which suits a demand that is mostly urban. The Fabra observatory (D5, Collserola, 410 m) is a forest site about 2 °C cooler on average than Raval, so using it shifts thresholds and slopes. Same 912 days, same method, slopes in GWh per °C:

  | Station | Area | Location | Altitude | Thresholds (cold / heat) | Slope cold | Slope heat | RMSE (GWh) |
  |---|---|---|---|---|---|---|---|
  | X4 Barcelona - el Raval (used) | Ciutat Vella, dense old town | Facultat de Geografia i Historia, c. Montalegre 6 (6th floor), 41.384 N 2.168 E | 33 m | 17 / 22 °C | 2.91 | 4.23 | 5.80 |
  | X8 Barcelona - Zona Universitaria | Les Corts, UB campus | Pistes UB, 41.379 N 2.105 E | 82 m | 17 / 21 °C | 2.54 | 3.90 | 5.76 |
  | D5 Barcelona - Observatori Fabra | Collserola hills, forest | Observatori Fabra, 41.419 N 2.124 E | 410 m | 15 / 19 °C | 2.42 | 3.22 | 6.20 |

  The two urban stations fit slightly better than Fabra. Other limits: one station for all of Catalonia, four years of data, no weekday or season correction, and the demand dataset covers the main distributor's network only.

## hydro_drought_replacement (.png, .svg): main figure 2

(a) Pyrenean rain (mean of 13 XEMA valley stations, 12-month total), Catalan hydro generation (12-month total) and the volume of the nine Conques Internes reservoirs, each as a percentage of its own 2019-2025 mean, with the 2022-2024 drought shaded (approximate). (b) Waterfall of the change in annual generation by source and in net imports from 2022 to 2023 (GWh); the steps add up to the change in total supply (-522 GWh). Hydro in blue, combined cycle in brown, net imports in red. The year-by-year changes for 2022-2025 are in Table 3 of the paper.

- **Data:** generation by technology from REData (REE); rain from XEMA daily precipitation (variable 1300), valley stations below 1,800 m in the Pyrenean comarques; net imports = electricity exchange balance from the Catalan energy indicators dataset (`j7xc-3kfh`). Code in `notebook/gabri_drought_hydro_energy.ipynb` and `notebook/xema.py`.
- **First reading:** hydro follows Pyrenean rain: both reach their minimum in 2023 and recover in 2024-2025 (annual hydro vs rain, r = 0.80, 7 years). The hypothesis "combined cycle replaces hydro in the drought" does not hold. 2022: hydro -704 GWh while combined cycle +3,097 (a gas-market and export episode, linked to the Iberian gas price cap) and net imports fall 1,285. 2023: hydro -458, combined cycle -2,014, nuclear -1,437, wind +623, and net imports rise 2,575: the gap is covered by imports. 2024: hydro +1,381 and combined cycle -1,042. 2025: small changes.
- **Context:** hydro is about 6% of Catalan generation in 2023, and nuclear about 60%, so its swings (for example longer refuelling outages at Asco in 2023, from press reports, not checked against official data) are as large as the hydro loss. Imports reach about 14% of demand in 2023 (press). Net imports in the dataset: 1,387 GWh (2019), 3,098 (2022), 5,672 (2023), 5,896 (2024), 6,227 (2025), consistent with demand minus local generation. Local generation falls from 45,112 GWh (2019) to 38,293 (2025) with flat demand, mostly combined cycle and cogeneration.
- **Limits:** correlation, not causation. Rain is a proxy: it ignores snow, altitude and reservoir management. Sources differ in definitions (REData generation and the indicators dataset), so changes do not add up exactly. The REData solar series may not include small rooftop installations (not checked).

## hydro_vs_rain (.png, .svg): supporting figure

Does hydro generation rise before the rain (anticipation) or after it (arrival of water)? Left: correlation of monthly anomalies (value minus the mean of the same calendar month) between hydro in month t and rain in month t - k. Right: hydro anomaly against the rain anomaly accumulated over the previous 6 months (r = 0.72).

- **Result:** the correlation peaks when rain leads hydro by 1 month (0.49) and 2 months (0.42), and is low when hydro leads rain (0.10 at one month, 0.14 at two). The k = -3 bar (0.30) most likely reflects wet and dry spells that persist for months, not anticipation. Hydro depends mostly on rain accumulated over the previous 6-12 months (r = 0.72 and 0.68), not on the current month.
- **Limits:** 84 months with strong autocorrelation, so a threshold of about 0.21 for significance is optimistic; rain is a mean over valley stations; at monthly resolution anticipation cannot be fully ruled out.

## energy_demand_vs_date (.png, .svg)

The same 912 days against the day of the year, coloured by temperature (coolwarm, centred on the comfort zone), with a seasonal curve that uses only the calendar (mean plus two annual harmonics, least squares).

- **Data and sample:** as `energy_demand_vs_temperature`. Code in `notebook/gabri_heat_energy_demand.ipynb`.
- **First reading:** on the same date, hotter or colder days use more electricity than the seasonal curve predicts. The calendar explains R² = 0.52 of the daily variation; the temperature fit explains 0.67, with fewer free parameters (3 coefficients plus 2 thresholds, against 5 coefficients). So temperature, not the date itself, drives most of the seasonal pattern.
- **Limits:** in-sample R², no cross-validation; the low points in early January and late December are the Christmas weeks, which neither model captures.

## energy_demand_by_hour (.png, .svg)

(a) Mean hourly demand profile on cold (< 12 °C), mild (17-22 °C) and hot (> 25 °C) days. (b) Demand at each hour and 2 °C temperature bin, as % above mild days at the same hour.

- **Data:** hourly columns `h01`-`h24` of `hx6q-ykhb` (MWh in each hour; `notebook/xema.py`, `download_demand_hourly`), taken as hours 0-23. The 24 hours add up exactly to the daily totals used above. Temperature is the daily mean at X4. Same 912 weekdays (no clock-change day falls among them); bins with fewer than 5 days hidden.
- **First reading:** heat adds most in the afternoon (up to about +35-40% around 13-17 h on days above 28 °C) and also keeps nights high; cold adds most in the morning (8-10 h) and evening peak (19-21 h).
- **Limits:** daily mean temperature, not hourly; the hour convention of `h01` (00-01 h) is assumed and should be checked in the dataset documentation. Next step: hourly temperature from XEMA.

## hydro_vs_reservoirs (.png, .svg): supporting figure

Monthly hydro generation, volume of the Conques Internes reservoirs, and monthly combined cycle and solar PV generation (same y axis), 2019-2025.

- **Data:** reservoirs from the Catalan open data dataset `gn9e-3qhr` (9 reservoirs, daily, averaged by month); basin percentage = total volume / total capacity (about 694 hm3), not the mean of the 9 percentages.
- **Reading:** the basin falls from about 95% (spring 2020) to about 15% in February 2024 and recovers to about 70-80% in 2025, but hydro follows it only loosely (annual correlation 0.69, monthly 0.50). In 2024 hydro grows 62% over 2023 while the basin is still at 25-35%. These are the reservoirs of the Conques Internes, not of the hydro basins: per Endesa (one operator, 2023-2024) they give about 2% of its Catalan hydro output, against about 25% for the Ebro basin and 73% for the Lleida region. Correlating hydro with each of the 9 reservoirs (monthly 0.39-0.58) or with Sau and Susqueda only (0.47) does not improve the link. Data for the Pyrenean reservoirs of the Ebro basin were not found in Catalan open data.

## olive_oil_vs_drought (Gabri/, .png and .svg)

Top: monthly olive oil consumer price index (2021 = 100), 2002-2025. Below: rain of each hydrological year (October to September) in Andalusia (Jaen, Cordoba) and in Catalonia (agricultural comarques), as a standardised anomaly (brown = drier than average, blue = wetter), 2003-2025.

- **Data:** INE monthly CPI by subclass, table 50905 (base 2021). The table 50937 named in the brief is the annual version, so it cannot give a lag in months. Rain in Catalonia: mean of 10 XEMA stations (variable 1300) in Segria, Garrigues, Priorat, Baix Ebre and Tarragones; rain in Andalusia: Open-Meteo reanalysis (ERA5-based, no key) at two grid points near Jaen and Cordoba, not station data (AEMET OpenData needs a personal key and was not used). Code in `notebook/gabri_drought_olive_oil.ipynb` and `notebook/xema.py`.
- **Checks with known values:** olive oil +54.6% and general CPI +3.1% in December 2023 match the official figures. The index peaks at 265 in April 2024 (annual change peak: +73.5% in October 2023) and falls to about 139 at the end of 2025.
- **Reading:** the driest hydrological years in Andalusia are 2005 (z = -1.90), 2012 (-1.03), 2019 (-0.98) and 2023 (-0.84). The December price change was +26.5%, +18.0%, -11.4% and +54.6%: three of the four driest years saw large price rises, 2019 did not. Other rises (2015 +26.5%, 2021 +26.7%, 2022 +35.2%) came with only mild deficits (z of -0.3 to -0.5), so other drivers matter. The wettest year (2010, z = +2.73) had a price change of -7.5%, and the fall of 2025 (-31.6%) came with a wet year.

## olive_oil_timeline (Gabri/, .png and .svg): paper figure 3

(a) Monthly annual change of the olive oil CPI and of the general CPI, 2003-2025, with the hydrological years of the four driest years in Andalusia (2005, 2012, 2019, 2023) shaded and the +73.5% peak (October 2023) marked. (b, c) The same scatter as `olive_oil_rain_vs_price_scatter` for Andalusia and Catalonia, with the least-squares line, the Pearson and Spearman coefficients in the panel title, and the notable years labelled. Same data and results as the two figures below.

## olive_oil_rain_vs_price_scatter (Gabri/, .png and .svg)

One point per year (2003-2025): rain anomaly of the hydrological year against the annual change of the olive oil CPI in December (the harvest runs from November to February), for Andalusia (left) and Catalonia (right). The shaded area marks drier-than-average years with rising prices.

- **Result:** Andalusia r = -0.42 (p = 0.047, n = 23; Spearman -0.33, p = 0.126). Catalonia r = -0.31 (p = 0.151; Spearman -0.15, p = 0.495). Our hypothesis that Andalusian rain explains the price better than Catalan rain holds in direction, but the evidence is borderline: it is significant only for the Pearson coefficient and only just, and the 23 years are not independent of the price cycle.
- **Choices made before looking at the result:** hydrological year (October-September) and the December price. Three analyses were run in total (monthly lags with 12 and 24-month windows, and this annual one) and all give weak to moderate negative correlations.

## olive_oil_lagged_correlation (Gabri/, .png and .svg)

Correlation between the annual change of the CPI of each product (olive oil, fresh fruit, fresh vegetables) at month t and the 12-month accumulated rain anomaly at month t - k, for k = 0 to 24 months, with rain in Andalusia (left) and in Catalonia (right). The strongest point for olive oil is marked.

- **Result (most negative correlation, the expected sign):** olive oil with Andalusian rain: r = -0.35 at a 7-month lag (12-month window) and at lag 0 (24-month window); with Catalan rain: r = -0.29 at lag 3 (12-month) and lag 0 (24-month). Fresh fruit: -0.26 at lag 13 (Andalusia) and -0.23 at lag 8 (Catalonia). Vegetables: about -0.1 to -0.3 without a clear lag. All correlations are weak (|r| of 0.35 or less, about 12% of the variance at most).
- **Reading:** Andalusian rain tracks olive oil prices slightly better than Catalan rain (-0.35 against -0.29), with a clearer dip at 6-8 months, but the difference is small. At long lags (above 15 months) the correlation turns positive, probably because of the multi-year cycle of prices, not a causal effect.
- **Limits (all three figures):** monthly series are strongly autocorrelated, so no significance can be claimed from them. Olive oil prices also depend on stocks, global markets, harvest size and base effects, not only on the rain of two regions. Rain is a proxy for the drought, not for the harvest; a better test would use the Spanish harvest (tonnes) or the rain of the flowering and fruit growth months.
