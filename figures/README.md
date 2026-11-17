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

## idea6_hydro_vs_reservoirs (.png, .svg)

Monthly hydro generation in Catalonia, volume of the Conques Internes reservoirs, and monthly combined cycle and solar PV generation (same y axis, so their sizes can be compared), 2019-2025, in three aligned panels. The grey band marks the 2022-2024 drought period (approximate) and the two minima are annotated.

- **Data:** generation by technology from REData (REE), Catalonia, monthly in MWh converted to GWh; reservoirs from the Catalan open data dataset `gn9e-3qhr` (9 reservoirs, daily, averaged by month). Basin percentage = total volume / total capacity (about 694 hm3), not the mean of the 9 percentages. Code in `notebook/gabri_idea6.ipynb` and `notebook/xema.py`.
- **First reading:** the basin falls from about 95% (spring 2020) to a minimum of about 15% in February 2024, and recovers to about 70-80% in 2025. Hydro generation follows these reservoirs only loosely (annual correlation 0.69, monthly 0.50): its lowest month is October 2023 (about 118 GWh) and it peaks every spring (about 690 GWh in May 2020). In 2024 hydro grows 62% over 2023 (2,220 to 3,600 GWh) while the basin is still at 25-35%.
- **Our hypothesis (combined cycle replaces hydro in the drought) does not hold.** Annual totals (GWh): hydro 3,382 (2021), 2,678 (2022), 2,220 (2023), 3,600 (2024); combined cycle 4,833, 7,930, 5,916, 4,873; solar PV 379, 385, 400, 422. Combined cycle jumps in 2022, but falls in 2023 (-25%) together with hydro (-17%), and in 2024 hydro recovers while combined cycle falls again. Possible reasons:
  1. **The reservoirs are not the hydro reservoirs.** The 9 reservoirs are the Conques Internes ones. Per Endesa (one operator, 2023-2024), the Ebro basin gives about 25% of its Catalan hydro output, the Lleida region about 73% and the Conques Internes about 2%. Its Catalan hydro output grew about 60% in 2024 thanks to the Ebro, Segre and Noguera Pallaresa, in line with the +62% above. Correlating hydro with each of the 9 reservoirs, or only Sau + Susqueda, does not improve the fit (monthly 0.39-0.58, Sau + Susqueda 0.47). Data for the Pyrenean reservoirs of the Ebro basin are not in Catalan open data (not found).
  2. **Hydro is small.** It is about 6% of Catalan generation in 2023, and its fall from 2021 to 2023 (1,162 GWh) is about 3% of the total, smaller than the swings in nuclear (-1,437 GWh in 2023, about 60% of the mix) and combined cycle (+3,097 in 2022, -2,014 in 2023).
  3. **Imports.** Net exchange balance (Catalan energy indicators, `j7xc-3kfh`, GWh): 1,387 (2019), 3,098 (2022), 5,672 (2023), 5,896 (2024), 6,227 (2025), consistent with demand minus local generation. In 2023 local generation falls 3,096 GWh, demand 901 GWh and imports rise 2,574 GWh. Press reports put imports at about 14% of Catalan demand in 2023.
  4. **2022 is a gas-market episode.** The Iberian gas price cap (June 2022) pushed gas power and exports to France up, so the combined cycle jump coincides with, but is probably not caused by, low hydro.
  5. **Structural decline of local generation:** total 45,112 GWh (2019) to 38,293 (2025) with flat demand; cogeneration 5,383 to 2,777 and combined cycle 8,764 to 5,633.
- **Limits:** correlation, not causation. The nuclear outage explanation (longer refuelling outages at Asco in 2023) comes from press reports, not checked against official data. The REData solar series may not include small rooftop installations (not checked). The Endesa share is one company, not all Catalan hydro. Monthly reservoir percentage is an average of daily values.
