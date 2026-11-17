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

Monthly hydro generation in Catalonia, reservoir volume of the Conques Internes basin, and monthly combined cycle and solar PV generation, 2019-2025, in three aligned panels.

- **Data:** generation by technology from REData (REE), Catalonia, monthly in MWh converted to GWh; reservoirs from the Catalan open data dataset `gn9e-3qhr` (9 reservoirs, daily, averaged by month). Basin percentage = total volume / total capacity (about 694 hm3), not the mean of the 9 percentages. Code in `notebook/gabri_idea6.ipynb` and `notebook/xema.py`.
- **First reading:** the basin falls from about 95% (spring 2020) to a minimum of about 15% in February 2024, and recovers to about 70-80% in 2025. Hydro generation follows the reservoirs only loosely: its lowest month is October 2023 (about 118 GWh), and it peaks every spring with the inflow (about 690 GWh in May 2020).
- **Who replaces hydro?** Annual totals (GWh): hydro 3,382 (2021), 2,678 (2022), 2,220 (2023), 3,600 (2024); combined cycle 4,833, 7,930, 5,916, 4,873; solar PV 379, 385, 400, 422. Combined cycle jumps in 2022 (summer peak above 1,000 GWh per month) when hydro falls, but in 2023 it falls too (-25%) while hydro falls (-17%), so there is no sign of replacement by combined cycle that year; in 2024 hydro recovers and combined cycle falls again. Solar PV is small on this scale (about 20-60 GWh per month) and grows slowly (+29% from 2022 to 2025).
- **Limits:** correlation, not causation: other drivers (exports, gas prices, nuclear and imports) are not in these data. The REData solar series may not include small rooftop installations (not checked). Monthly reservoir percentage is an average of daily values.
