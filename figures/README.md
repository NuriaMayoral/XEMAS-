# Figures

## idea6_demand_vs_temperature (.png, .svg)

Daily electricity demand in Catalonia against mean daily temperature, coloured by season, with a two-threshold piecewise linear fit.

- **Data:** demand from the Catalan open data dataset `hx6q-ykhb` (daily total, MWh, converted to GWh); temperature from XEMA daily data (`7bvh-jvq2`, variable 1000) at station X4, Barcelona - el Raval. Code in `notebook/gabri_idea6.ipynb` and `notebook/xema.py`.
- **Sample:** weekdays 2022-2025 (912 days), excluding Catalan public holidays, August (holiday effect) and 28 Apr 2025 (Iberian blackout, 69 GWh).
- **First reading:** comfort zone between 17 and 22 °C (about 114 GWh/day). Demand rises about 2.9 GWh per °C below 17 °C and about 4.2 GWh per °C above 22 °C, so heat weighs more than cold. At the same temperature winter days consume more than spring days, so temperature explains only part of the variation (residual RMSE about 5.8 GWh).
- **Choice of station:** Raval is urban (33 m), which suits a demand that is mostly urban. The Fabra observatory (D5, Collserola, 410 m) is a forest site about 2 °C cooler on average than Raval, so using it shifts thresholds and slopes. Same 912 days, same method, slopes in GWh per °C:

  | Station | Area | Location | Altitude | Thresholds (cold / heat) | Slope cold | Slope heat | RMSE (GWh) |
  |---|---|---|---|---|---|---|---|
  | X4 Barcelona - el Raval (used) | Ciutat Vella, dense old town | Facultat de Geografia i Historia, c. Montalegre 6 (6th floor), 41.384 N 2.168 E | 33 m | 17 / 22 °C | 2.91 | 4.23 | 5.80 |
  | X8 Barcelona - Zona Universitaria | Les Corts, UB campus | Pistes UB, 41.379 N 2.105 E | 82 m | 17 / 21 °C | 2.54 | 3.90 | 5.76 |
  | D5 Barcelona - Observatori Fabra | Collserola hills, forest | Observatori Fabra, 41.419 N 2.124 E | 410 m | 15 / 19 °C | 2.42 | 3.22 | 6.20 |

  The two urban stations fit slightly better than Fabra. Other limits: one station for all of Catalonia, four years of data, no weekday or season correction, and the demand dataset covers the main distributor's network only.

## idea6_hydro_drought_replacement (.png, .svg): main figure 2

Top: Pyrenean rain (mean of 13 XEMA valley stations, 12-month total) and Catalan hydro generation (12-month total), 2019-2025, with the 2022-2024 drought period shaded (approximate). Bottom: change in annual generation by source, and in net imports, versus the previous year, for 2022-2025, all on the same GWh scale (hydro in blue, net imports in red).

- **Data:** generation by technology from REData (REE); rain from XEMA daily precipitation (variable 1300), valley stations below 1,800 m in the Pyrenean comarques; net imports = electricity exchange balance from the Catalan energy indicators dataset (`j7xc-3kfh`). Code in `notebook/gabri_idea6.ipynb` and `notebook/xema.py`.
- **First reading:** hydro follows Pyrenean rain: both reach their minimum in 2023 and recover in 2024-2025 (annual hydro vs rain, r = 0.80, 7 years). The hypothesis "combined cycle replaces hydro in the drought" does not hold. 2022: hydro -704 GWh while combined cycle +3,097 (a gas-market and export episode, linked to the Iberian gas price cap) and net imports fall 1,285. 2023: hydro -458, combined cycle -2,014, nuclear -1,437, wind +623, and net imports rise 2,575: the gap is covered by imports. 2024: hydro +1,381 and combined cycle -1,042. 2025: small changes.
- **Context:** hydro is about 6% of Catalan generation in 2023, and nuclear about 60%, so its swings (for example longer refuelling outages at Asco in 2023, from press reports, not checked against official data) are as large as the hydro loss. Imports reach about 14% of demand in 2023 (press). Net imports in the dataset: 1,387 GWh (2019), 3,098 (2022), 5,672 (2023), 5,896 (2024), 6,227 (2025), consistent with demand minus local generation. Local generation falls from 45,112 GWh (2019) to 38,293 (2025) with flat demand, mostly combined cycle and cogeneration.
- **Limits:** correlation, not causation. Rain is a proxy: it ignores snow, altitude and reservoir management. Sources differ in definitions (REData generation and the indicators dataset), so changes do not add up exactly. The REData solar series may not include small rooftop installations (not checked).

## idea6_hydro_vs_rain (.png, .svg): supporting figure

Does hydro generation rise before the rain (anticipation) or after it (arrival of water)? Left: correlation of monthly anomalies (value minus the mean of the same calendar month) between hydro in month t and rain in month t - k. Right: hydro anomaly against the rain anomaly accumulated over the previous 6 months (r = 0.72).

- **Result:** the correlation peaks when rain leads hydro by 1 month (0.49) and 2 months (0.42), and is low when hydro leads rain (0.10 at one month, 0.14 at two). The k = -3 bar (0.30) most likely reflects wet and dry spells that persist for months, not anticipation. Hydro depends mostly on rain accumulated over the previous 6-12 months (r = 0.72 and 0.68), not on the current month.
- **Limits:** 84 months with strong autocorrelation, so a threshold of about 0.21 for significance is optimistic; rain is a mean over valley stations; at monthly resolution anticipation cannot be fully ruled out.

## idea6_hydro_vs_reservoirs (.png, .svg): supporting figure

Monthly hydro generation, volume of the Conques Internes reservoirs, and monthly combined cycle and solar PV generation (same y axis), 2019-2025.

- **Data:** reservoirs from the Catalan open data dataset `gn9e-3qhr` (9 reservoirs, daily, averaged by month); basin percentage = total volume / total capacity (about 694 hm3), not the mean of the 9 percentages.
- **Reading:** the basin falls from about 95% (spring 2020) to about 15% in February 2024 and recovers to about 70-80% in 2025, but hydro follows it only loosely (annual correlation 0.69, monthly 0.50). In 2024 hydro grows 62% over 2023 while the basin is still at 25-35%. These are the reservoirs of the Conques Internes, not of the hydro basins: per Endesa (one operator, 2023-2024) they give about 2% of its Catalan hydro output, against about 25% for the Ebro basin and 73% for the Lleida region. Correlating hydro with each of the 9 reservoirs (monthly 0.39-0.58) or with Sau and Susqueda only (0.47) does not improve the link. Data for the Pyrenean reservoirs of the Ebro basin were not found in Catalan open data.
