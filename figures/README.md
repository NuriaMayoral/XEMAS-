# Figures

## idea6_demand_vs_temperature (.png, .svg)

Daily electricity demand in Catalonia against mean daily temperature, coloured by season, with a two-threshold piecewise linear fit.

- **Data:** demand from the Catalan open data dataset `hx6q-ykhb` (daily total, MWh, converted to GWh); temperature from XEMA daily data (`7bvh-jvq2`, variable 1000) at station D5, Barcelona-Fabra. Code in `notebook/gabri_idea6.ipynb` and `notebook/xema.py`.
- **Sample:** weekdays 2022-2025 (912 days), excluding Catalan public holidays, August (holiday effect) and 28 Apr 2025 (Iberian blackout, 69 GWh).
- **First reading:** comfort zone between 15 and 19 °C (about 114 GWh/day). Demand rises about 2.4 GWh per °C below 15 °C and about 3.2 GWh per °C above 19 °C, so heat weighs more than cold. At the same temperature winter days consume more than spring days, so temperature explains only part of the variation (residual RMSE about 6 GWh).
- **Caveat on the station:** Fabra is at 410 m in Collserola (forest), on average about 2 °C cooler than the urban stations X4 (Raval) and X8 (Zona Universitaria). Thresholds and slopes depend on the thermometer. Same 912 days, same method:

  | Station | Thresholds (cold / heat) | Slope cold | Slope heat | RMSE (GWh) |
  |---|---|---|---|---|
  | D5 Fabra (410 m) | 15 / 19 °C | 2.42 | 3.22 | 6.20 |
  | X4 Raval (33 m) | 17 / 22 °C | 2.91 | 4.23 | 5.80 |
  | X8 Zona Univ. (82 m) | 17 / 21 °C | 2.54 | 3.90 | 5.76 |

  Slopes are in GWh per °C. The urban stations fit slightly better. Other limits: one station for all of Catalonia, four years of data, no weekday or season correction, and the demand dataset covers the main distributor's network only.
