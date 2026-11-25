# Drought and heat in Catalonia: effects on water, crops, forest fires and electricity

*How do drought and heat in Catalonia affect water reserves, crops, forest fires and electricity use?*

**Team:** Gabriel Albasini (@gabrielvalbasini-lab) · Núria Mayoral (@NuriaMayoral) · Jesús Ruiz (@jesusruango-dev) · Hug Sala (@hugsalaoriol)

## Question

How do drought and heat in Catalonia affect water reserves, crops, forest fires and electricity use? We use daily data from the XEMA weather stations and other open data from the Generalitat de Catalunya and Idescat. Each member studies one effect: reservoirs and drought status (Núria), crop yields (Hug), burned area (Jesús) and electricity demand (Gabriel). Knowing when these effects appear can help to plan for dry and hot periods.

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
| `raw/xema_<station>_1000_2019-01-01_2025-12-31.csv` | Daily mean temperature (XEMA variable 1000, °C) at three Barcelona stations, 2019-2025: X4 el Raval (used in the main fit), X8 Zona Universitària and D5 Observatori Fabra (station check). One file per station (date, value; 2,556-2,557 rows each). Station names, altitude and coordinates read from `yqwd-vj5e` | [Transparència Catalunya `7bvh-jvq2`](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-di-ries-de-la-XEMA/7bvh-jvq2/about_data) (Meteocat) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17 | `gabri_heat_energy_demand.ipynb` |
| `raw/demand_2019-01-01_2025-12-31.csv`, `raw/demand_hourly_2022-01-01_2025-12-31.csv` | Daily electricity demand in Catalonia, MWh, 2019-2025 (2,557 rows × 2), and the hourly columns `h01`-`h25` of the same dataset, 2022-2025 (1,461 rows × 26). Network of the main distributor only; until September 2021 it also included energy passed on to other distributors | [Transparència Catalunya `hx6q-ykhb`](https://analisi.transparenciacatalunya.cat/d/hx6q-ykhb) (ICAEN) | [Llicència oberta d'ús d'informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (attribution) | 2026-11-17, 2026-11-18 | `gabri_heat_energy_demand.ipynb` |

Notes:

- Numbers in the CSVs use a comma as decimal separator (and a dot for thousands in some columns), so read them with `decimal=","` and `thousands="."`.
- The municipality code in the fires CSV has no leading zero (e.g. `80018`); pad it to 6 digits before joining with the maps.
- Comarques names (also refered as counties/regions along the code) change between the Idescat yearly files, so they are harmonised (`harmonise()`). Yield is recomputed as production divided by area. Crop names also vary along the different files. 
- The XEMA daily data are downloaded through the open data API the first time (`download_daily(2007, 2025)`), so that first run needs internet and may take a while.
- The `raw/` files of Gabriel's rows are not in Git (`data/raw/` is git-ignored). `src/xema.py` downloads each one from its API the first time the notebook asks for it and saves it as CSV in `data/raw/`; later runs read that copy. So the first run needs internet, and anyone can rebuild the files by running the notebook. No API key is needed.

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

Gabriel's analysis is the notebook `notebook/gabri_heat_energy_demand.ipynb`, run from the `notebook/` folder. It imports `src/xema.py` (download and cache helpers) and uses pandas, numpy, matplotlib, requests and holidays (`uv pip install -r requirements.txt holidays`). The first run downloads the raw data (see the notes under the data table). It saves the three figures `figures/Gabri/energy_demand_*.png`; the notebook explains each one and its limits.

## Figures

| Figure | File | Message |
|---|---|---|
| fires_map_municipalities | `figures/fires_map_municipalities.png` | Map with the forest hectares burned in Catalonia for every municipality for 2011-2024. |
| fires_map_regions | `figures/fires_map_regions.png` | Map with the forest hectares burned in Catalonia for every comarca for 2011-2024. |
| energy_demand_vs_temperature | `figures/Gabri/energy_demand_vs_temperature.png` | Shows that catalan electricity demand is flat between 17 and 22 °C and rises faster with heat than with cold. |
| energy_demand_vs_date | `figures/Gabri/energy_demand_vs_date.png` | Shows that temperature explains more of the daily variation in demand than the date alone (R² = 0.67 against 0.52). |
| energy_demand_by_hour | `figures/Gabri/energy_demand_by_hour.png` | Shows that heat adds demand in the afternoon, and cold in the morning and evening. |
| time_panel | `figures/Hug/time_panel.png` | Rainfall, temperature and yield anomalies of wheat by year: dry years such as 2023 coincide with low yields. |
| scatter_panel | `figures/Hug/scatter._panelpng` | Yield anomaly against rainfall anomaly for four crops: yield increases with rainfall for wheat, with little or no response for olive, and a small decrease for vine. |
| maps_panel | `figures/Hug/maps_panel.png` | Maps of rainfall and crop yield anomalies per comarca per crop for selected years (2015, 2020, 2023). |

## Use of AI tools

Claude Sonnet 5.5 was used by Gabriel to:
- Learn how to use git commands. 
- Help with downloading databases.
- Check and fix code, and suggest using np.clip to do three separate fits in 'notebook/gabri_heat_energy_demand.ipynb'.
- Help with English wording and grammar in minipaper and presentation.

Claude Sonnet 5.5 was used by Hug to:
- Help with code writting of data cleaning functions
- Code fixing and model suggestions
- Rephrasing suggestions for minipaper

Initial question and database selection, code structure and workflow, analysis and model choices, figure ideas and full README, minipaper draft and presentation slides were entirely ours.

## Licence

Code: see `LICENSE`. 
Data: see the licences in the table above.