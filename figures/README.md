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

## idea4_olive_oil_vs_drought (.png, .svg)

Olive oil CPI (annual change, %) and the 24-month accumulated rain anomaly (z-score, negative = drier than usual) in Andalusia and in Catalonia, 2015-2025, with the 2022-2024 drought period shaded (approximate).

- **Data:** INE monthly CPI by subclass, table 50905 (base 2021, 2002-2025). The table 50937 named in the brief is the annual version of the same data, so it cannot give a lag in months. Rain in Catalonia: mean of 10 XEMA stations (variable 1300) in Segria, Garrigues, Priorat, Baix Ebre and Tarragones; rain in Andalusia: Open-Meteo reanalysis (ERA5-based, no key) at two grid points near Jaen and Cordoba, not station data (AEMET OpenData needs a personal key and was not used). Code in `notebook/gabri_idea4.ipynb` and `notebook/xema.py`.
- **Check with known values:** olive oil +54.6% and general CPI +3.1% in December 2023 match the official figures. The olive oil peak is +73.5% in October 2023, and the series falls to about -45% in mid-2025.
- **First reading:** the price rise starts in 2021, before the drought period, and peaks in autumn 2023. The Andalusian anomaly stays between about -0.3 and -1.2 from mid-2020 to 2024, a moderate deficit; the Catalan anomaly is positive in 2020-2021 and reaches its minimum (-2.1) in early 2024, after the price peak. Prices fall in 2024-2025 when rain returns (positive anomalies in 2025). Annual changes include base effects: after a spike, a fall is partly mechanical.

## idea4_lagged_correlation (.png, .svg)

Correlation between the annual change of the CPI of each product (olive oil, fresh fruit, fresh vegetables) at month t and the 12-month accumulated rain anomaly at month t - k, for k = 0 to 24 months, with rain in Andalusia (left) and in Catalonia (right).

- **Result (most negative correlation, the expected sign):** olive oil with Andalusian rain: r = -0.35 at a 7-month lag (12-month window) and at lag 0 (24-month window); with Catalan rain: r = -0.29 at lag 3 (12-month) and lag 0 (24-month). Fresh fruit: -0.26 at lag 13 (Andalusia) and -0.23 at lag 8 (Catalonia). Vegetables: about -0.1 to -0.3 without a clear lag. All correlations are weak (|r| of 0.35 or less, so about 12% of the variance at most).
- **Reading:** Andalusian rain tracks olive oil prices slightly better than Catalan rain (-0.35 against -0.29), and its curve has a clearer dip at 6-8 months, but the difference is small. At long lags (above 15 months) the olive oil correlation turns positive, probably because of the multi-year cycle of harvests and prices, not a causal effect.
- **Limits:** monthly series are strongly autocorrelated, so the number of independent observations is much smaller than 288 and no significance can be claimed. Olive oil prices also depend on stocks, global markets, harvest size and base effects, not only on the rain of two regions. Rain accumulated over 12 months is a proxy for the drought, not for the harvest. A better test would use the Spanish harvest (tonnes) or rain in the months of flowering and fruit growth.

## idea2_income_shelters_map (.png, .svg)

Choropleth of disposable income per person (2023) by census section in Barcelona, with the 564 climate shelters as red points.

- **Data (Open Data BCN):** income by census section, 2023 (`renda-disponible-llars-bcn`, 1,068 sections); climate shelters network (`xarxa-refugis-climatics`, 564 points with coordinates in EPSG:25831, the CSV is encoded in UTF-16); census section polygons (`20170706-districtes-barris`); population by section on 1 January 2024 (`pad_mdbas_sexe`, 1,702,814 inhabitants). The three section tables match one to one. Section ids are district x 1000 + section, because the income file numbers the sections within each district. Code in `notebook/gabri_idea2.ipynb` and `notebook/opendata_bcn.py`.
- **First reading:** the highest incomes (above about 40,000 EUR) are in the west of the city (Sarria-Sant Gervasi, Les Corts and part of the Eixample); the lowest are in the north-east (Nou Barris, Sant Andreu) and Ciutat Vella. Shelters are spread over the whole city and dense in the centre. The network mixes covered pools, libraries, nursery school yards, water play areas and civic centres, so not all shelters are equivalent (opening hours are not considered).

## idea2_accessibility_by_income (.png, .svg)

Share of the population within 400 m (about 5 min) and 800 m (about 10 min) in a straight line of the nearest climate shelter, by income decile (deciles weighted by population, about 10% of the population each; decile 1 = lowest income).

- **Method:** share of each section's area inside the 400 m and 800 m buffers of the shelters, times the section's population (population assumed uniform inside a section; EPSG:25831). A second measure (distance from one point of each section) gives the same pattern.
- **Result:** the whole city has 96.6% of the population within 400 m and 99.5% within 800 m, consistent with the official claim of 99% within 10 minutes in a straight line. The poorest deciles are well served (97% within 400 m and 99-100% within 800 m in decile 1). The richest decile has the lowest coverage: 88.3% within 400 m and 98.6% within 800 m (point measure: 88.5% and 99.0%). Spearman correlation between income and distance to the nearest shelter: +0.07 (very weak). Our initial hypothesis (poorer areas have fewer shelters nearby) is not supported.
- **Why decile 10 is lower:** it is 63% Sarria-Sant Gervasi and 11% Les Corts, with low density (median 22,700 inhabitants per km2 against about 45,000 in the other deciles) and larger sections (median 6.7 ha against about 3.5). Shelters per 10,000 residents by district: Ciutat Vella 4.9, Sant Andreu 4.8, Eixample 3.5, Les Corts 3.4, Nou Barris 3.2, Sants-Montjuic 3.0, Gracia 2.9, Sant Marti 2.8, Horta-Guinardo 2.7, Sarria-Sant Gervasi 2.6. Area-based coverage is the lowest in Les Corts (88.7%) and Sarria-Sant Gervasi (91.1%).
- **Limits:** straight-line distance understates the walk along the street network (a network analysis is the next step). Uniform density inside a section penalises sections with large non-residential areas (parks, hillsides). Access is not exposure: this analysis does not measure temperature, which would require, for example, Landsat surface temperature on a heatwave day. Shelter quality, capacity and opening hours are not considered.
