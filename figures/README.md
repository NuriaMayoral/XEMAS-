# Figures

This file describes Gabriel's figures. Other figures: `fires_map_*.png` (Jesús), `Hug/` and `nuria/`, documented in their notebooks and in the main `README.md`.

Gabriel's figures are saved in the `Gabri/` folder (PNG at 200 dpi). All three come from `notebook/gabri_heat_energy_demand.ipynb`. Their colours are colour-blind safe (Okabe-Ito, coolwarm, cividis).

## energy_demand_vs_temperature (.png): main figure

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

## energy_demand_vs_date (.png)

The same 912 days against the day of the year, coloured by temperature (coolwarm, centred on the comfort zone), with a seasonal curve that uses only the calendar (mean plus two annual harmonics, least squares).

- **Data and sample:** as `energy_demand_vs_temperature`. Code in `notebook/gabri_heat_energy_demand.ipynb`.
- **First reading:** on the same date, hotter or colder days use more electricity than the seasonal curve predicts. The calendar explains R² = 0.52 of the daily variation; the temperature fit explains 0.67, with the same number of free parameters (3 coefficients plus 2 thresholds, against 5 coefficients). So temperature, not the date itself, drives most of the seasonal pattern.
- **Limits:** in-sample R², no cross-validation; the low points in early January and late December are the Christmas weeks, which neither model captures.

## energy_demand_by_hour (.png)

(a) Mean hourly demand profile on cold (< 12 °C), mild (17-22 °C) and hot (> 25 °C) days; the demand axis starts at 0 GW. (b) Demand at each hour and 2 °C temperature bin, as % above mild days at the same hour.

- **Data:** hourly columns `h01`-`h24` of `hx6q-ykhb` (MWh in each hour; `notebook/xema.py`, `download_demand_hourly`), taken as hours 0-23. The 24 hours add up exactly to the daily totals used above. Temperature is the daily mean at X4. Same 912 weekdays (no clock-change day falls among them); bins with fewer than 5 days hidden.
- **First reading:** heat adds most in the afternoon, 13-17 h: about +31-34% on days of 28-30 °C and +36-40% on days of 30-32 °C (6 days), and it also keeps nights high. Cold adds most in the morning (8-11 h) and in the evening (18-20 h): about +24-26% on days of 8-10 °C.
- **Limits:** daily mean temperature, not hourly; the hour convention of `h01` (00-01 h) is assumed and should be checked in the dataset documentation. Next step: hourly temperature from XEMA.
