# Project title

*One sentence: the question your project answers.*

**Team:** Gabriel Albasini (@gabrielvalbasini-lab) · Núria Mayoral (@NuriaMayoral) · Jesús Ruiz (@jesusruango-dev) · Hug Sala (@hugsalaoriol)

## Question

What you want to find out and why it matters (3–5 sentences).

# Data

Everything the notebooks need is in this folder, so they run offline. Files written by the notebooks go to `../figures/`, never here.

## Files

| Path | What | Source | Licence / terms | Retrieved | Used in |
|---|---|---|---|---|---|
| `Incendis_forestals_a_Catalunya__Anys_2011-2024_20261116.csv` | Forest fires in Catalonia, 2011-2024 (7,545 rows × 9 columns) | [Transparència Catalunya `bks7-dkfd`](https://analisi.transparenciacatalunya.cat/Medi-Rural-Pesca/Incendis-forestals-a-Catalunya-Anys-2011-2024/bks7-dkfd/about_data) (Generalitat de Catalunya) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-16 | map_fires_municipalities, map_fires_regions |
| `divisions-administratives-v2r1-municipis-1000000-20250730.json` | Municipality outlines of Catalonia (1:1,000,000), EPSG:4326 | [ICGC, Divisions administratives v2r1 (2025-07-30)](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) | ICGC terms of use (attribution) | 2025-07-30 | map_fires_municipalities |
| `divisions-administratives-v2r1-comarques-250000-20250730.json` | Comarca outlines of Catalonia (1:250,000), EPSG:4326 | [ICGC, Divisions administratives v2r1 (2025-07-30)](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) | ICGC terms of use (attribution) | 2025-07-30 | map_fires_regions |
| `Sequera_Catalunya.csv` | Drought status changes per municipality and exploitation unit, 2021-2025 (8,677 rows; hydrological and pluviometric status) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | TODO | — |
| `Quantitat_d_aigua_als_embassaments_Catalunya.csv` | Daily water level, stored volume (hm3) and percentage of capacity in 9 reservoirs of the Catalan internal basins, 2000-2026 (88,308 rows) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | TODO | — |
| `Aigües_subterrànies_de_Catalunya.csv` | Groundwater monitoring: water depth and piezometric level per station and date, with coordinates and municipality (244,538 rows) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | TODO | — |
| `crops_all_years.csv` | Processed crop data of Catalonia, 2008-2025, from yearly xlsx files (`Produccions_comarcals_yyyy.xlsx`). Surface and production per crop, year, cultivation method and comarca, column of codes for each, with yield recomputed as production / area. | [Idescat, Estadística agrària: superfície i producció de cultius per comarca](https://agricultura.gencat.cat/ca/departament/observatori-agroambiental/estadistiques/agricultura/estadistiques-definitives-conreus/) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 18-11-2026 | `hug_idescat_loader.py`, `hug_climate_yield.py`, `hug_plots.py`, `hug_load_data.ipynb` |
| `https://analisi.transparenciacatalunya.cat/resource/7bvh-jvq2.json` | Daily temperature and precipitation of the XEMA weather stations, 2007-2025. Through API. | [Transparència Catalunya `7bvh-jvq2`](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-di-ries-de-la-XEMA/7bvh-jvq2/about_data) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 10-11-2026 | `hug_climate_yield.py`, `hug_plots.py`, `hug_load_data.ipynb` |
| `https://analisi.transparenciacatalunya.cat/resource/yqwd-vj5e.json` | XEMA station metadata (code, name, coordinates, comarca). Through API | [Transparència Catalunya `yqwd-vj5e`](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Metadades-estacions-meteorol-giques-autom-tiques/yqwd-vj5e/about_data) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 10-11-2026 | `hug_climate_yield.py`, `hug_plots.py`, `hug_load_data.ipynb` |
| `raw/generation_2019_2025.csv` | Monthly electricity generation in Catalonia by technology, 2019-2025, in MWh (920 rows × 3: date, technology, value; 11 series, solar thermal misses 4 months) | [REData API, Red Eléctrica (REE)](https://www.ree.es/es/apidatos), endpoint `generacion/estructura-generacion` | No open licence stated; the [REE legal notice](https://www.ree.es/es/aviso-legal) allows academic use citing REE as source | 2026-11-17 | `gabri_drought_hydro_energy.ipynb`, `gabri_figures_v2.py` |
| `raw/xema_<station>_<variable>_<start>_<end>.csv` | XEMA daily data used by Gabri, one file per station and variable (date, value; 26 files, 1.9 MB): mean temperature (variable 1000) at X4, X8 and D5, 2019-2025; precipitation (variable 1300) at 13 Pyrenean valley stations (Y4, W5, CJ, CD, CT, DP, YA, WQ, CP, XQ, YC, XH, YG), 2019-2025, and at 10 stations in the agricultural comarques (VK, VH, WK, UM, D1, WJ, U7, DB, VQ, DK), 2002-2025. Station metadata read from `yqwd-vj5e` | [Transparència Catalunya `7bvh-jvq2`](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-di-ries-de-la-XEMA/7bvh-jvq2/about_data) (Meteocat) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17 | `gabri_heat_energy_demand.ipynb`, `gabri_drought_hydro_energy.ipynb`, `gabri_drought_olive_oil.ipynb`, `gabri_figures_v2.py` |
| `raw/demand_2019-01-01_2025-12-31.csv`, `raw/demand_hourly_2022-01-01_2025-12-31.csv` | Daily electricity demand in Catalonia, MWh, 2019-2025 (2,557 rows × 2), and the hourly columns `h01`-`h25` of the same dataset, 2022-2025 (1,461 rows × 26) | [Transparència Catalunya `hx6q-ykhb`](https://analisi.transparenciacatalunya.cat/d/hx6q-ykhb) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17, 2026-11-18 | `gabri_heat_energy_demand.ipynb` |
| `raw/reservoirs_2019-01-01_2025-12-31.csv` | Daily stored volume (hm3) and percentage of capacity of the 9 Conques Internes reservoirs, 2019-2025 (23,013 rows × 4) | [Transparència Catalunya `gn9e-3qhr`](https://analisi.transparenciacatalunya.cat/d/gn9e-3qhr) (ACA) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17 | `gabri_drought_hydro_energy.ipynb`, `gabri_figures_v2.py` |
| `raw/indicators_2019-01-01_2025-12-31.csv` | Monthly Catalan energy indicators: net electricity exchange balance (net imports) and electricity demand, GWh, 2019-2025 (84 rows × 3) | [Transparència Catalunya `j7xc-3kfh`](https://analisi.transparenciacatalunya.cat/d/j7xc-3kfh) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17 | `gabri_drought_hydro_energy.ipynb`, `gabri_figures_v2.py` |
| `raw/cpi_50905.csv` | Monthly consumer price index of Spain (base 2021): index and annual change (%) of olive oil, fresh fruit, fresh vegetables and the general index, 2002-2025 (288 rows × 9) | [INE table 50905](https://www.ine.es/jaxiT3/Tabla.htm?t=50905), through the INE JSON API (`servicios.ine.es/wstempus`) | CC BY 4.0 ([INE legal notice](https://www.ine.es/dyngs/AYU/index.htm?cid=125)) | 2026-11-17 | `gabri_drought_olive_oil.ipynb`, `gabri_figures_v2.py` |
| `raw/rain_openmeteo_<site>_2002-01-01_2025-12-31.csv` | Daily precipitation (mm) at two reanalysis grid points near Jaén (37.77 N, 3.79 W) and Córdoba (37.89 N, 4.78 W), 2002-2025 (8,766 rows × 2 each) | [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) (default "best match" of ERA5, ERA5-Land and IFS) | CC BY 4.0 ([Open-Meteo licence](https://open-meteo.com/en/licence)); free API for non-commercial use | 2026-11-17 | `gabri_drought_olive_oil.ipynb`, `gabri_figures_v2.py` |

Notes:

- Numbers in the CSVs use a comma as decimal separator (and a dot for thousands in some columns), so read them with `decimal=","` and `thousands="."`.
- The municipality code in the fires CSV has no leading zero (e.g. `80018`); pad it to 6 digits before joining with the maps.
- Comarques names (also refered as counties/regions along the code) change between the Idescat yearly files, so they are harmonised (`harmonise()`). Yield is recomputed as production divided by area. Crop names also vary along the different files. 
- The XEMA daily data are downloaded through the open data API the first time (`download_daily(2007, 2025)`), so that first run needs internet and may take a while.
- The `raw/` files of Gabri's rows are not in Git (`data/raw/` is git-ignored). `notebook/xema.py` downloads each one from its API the first time a notebook asks for it and saves it as CSV in `data/raw/`; later runs read that copy. So the first run needs internet, and anyone can rebuild the files by running the notebooks. No API key is needed.

## Repositories of open datasets

### Open data portals

- [Transparència Catalunya](https://analisi.transparenciacatalunya.cat/) · [ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) · [Idescat](https://www.idescat.cat/)

- ## How to run

```console
git clone https://github.com/NuriaMayoral/XEMAS-.git
cd <XEMAS->
uv sync            # or: conda env create -f environment.yml
uv run jupyter lab
```

The crop and weather analysis is in `hug_load_data.ipynb`. It imports the scripts in `src/` (`hug_idescat_loader.py`, `hug_climate_yield.py`, `hug_plots.py`). On the first run, download the daily weather data with `C.download_daily(2007, 2025)` (2007 is needed because the 2008 cereal season starts in October of the previous year). For crop data, there are 2 options:
- Download xlsx files from [Idescat, Estadística agrària: superfície i producció de cultius per comarca](https://agricultura.gencat.cat/ca/departament/observatori-agroambiental/estadistiques/agricultura/estadistiques-definitives-conreus/) into folder `data/raw/`. 
- Use the pre-downloaded data in `crops_all_years.csv` and start the analysis in `hug_load_data.ipynb` from section "Using preparated dataset".

Gabri's analyses are three notebooks in `notebook/`, run from that folder (*Kernel → Restart & Run All*), in any order:

1. `gabri_heat_energy_demand.ipynb`: electricity demand and temperature (`figures/Gabri/energy_demand_*`)
2. `gabri_drought_hydro_energy.ipynb`: drought, hydropower and imports (`figures/Gabri/hydro_*`)
3. `gabri_drought_olive_oil.ipynb`: rain and olive oil prices (`figures/Gabri/olive_oil_*`)

They import `xema.py` (download and cache helpers) and `gabri_figures_v2.py`, which draws the two main figures `hydro_drought_replacement` and `olive_oil_timeline` (it can also be run alone: `cd notebook && python gabri_figures_v2.py`). They use pandas, numpy, matplotlib, scipy, requests and holidays (`uv pip install -r requirements.txt holidays`). The first run downloads the raw data (see the notes under the data table). What each figure shows and its limits are in `figures/README.md`.

## Figures

| Figure | File | Message |
|---|---|---|
| fires_map_municipalities | `figures/fires_map_municipalities.png` | Map with the forest hectares burned in Catalonia for every municipality for 2011-2024. |
| fires_map_regions | `figures/fires_map_regions.png` | Map with the forest hectares burned in Catalonia for every comarca for 2011-2024. |
| energy_demand_vs_temperature | `figures/Gabri/energy_demand_vs_temperature.png` | Catalan electricity demand is flat between 17 and 22 °C and rises faster with heat (+3.7% per °C) than with cold (+2.5% per °C). |
| hydro_drought_replacement | `figures/Gabri/hydro_drought_replacement.png` | Hydropower followed Pyrenean rain down in the 2022-2024 drought, and in 2023 the gap was covered by imports, not by gas plants. |
| olive_oil_timeline | `figures/Gabri/olive_oil_timeline.png` | Olive oil prices rose after three of the four driest years in Andalusia, but the link with rain is weak (r = -0.42, 23 years). |

## Use of AI tools

- Which tools you used, for what (e.g. *drafting the pagination loop in `src/download.py`*).
- What you checked (row counts, units, CRS, every line in `src/`).
- What is entirely yours (question, analysis choices, text).

## Licence

Code: see `LICENSE`. 
Data: see the licences in the table above.