# Project title

*One sentence: the question your project answers.*

**Team:** Gabriel Vicente Albasini Surname (@gabrielvalbasini-lab) · Núria Mayoral (@NuriaMayoral) · Jesús Ruiz (@jesusruango-dev) · Hug Sala (@hugsalaoriol)

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

Notes:

- Numbers in the CSVs use a comma as decimal separator (and a dot for thousands in some columns), so read them with `decimal=","` and `thousands="."`.
- The municipality code in the fires CSV has no leading zero (e.g. `80018`); pad it to 6 digits before joining with the maps.
- Comarques names (also refered as counties/regions along the code) change between the Idescat yearly files, so they are harmonised (`harmonise()`). Yield is recomputed as production divided by area. Crop names also vary along the different files. 
- The XEMA daily data are downloaded through the open data API the first time (`download_daily(2007, 2025)`), so that first run needs internet and may take a while.

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

## Figures

| Figure | File | Message |
|---|---|---|
| fires_map_municipalities | `figures/fires_map_municipalities.png` | Map with the forest hectares burned in Catalonia for every municipality for 2011-2024. |
| fires_map_regions | `figures/fires_map_regions.png` | Map with the forest hectares burned in Catalonia for every comarca for 2011-2024. |

## Use of AI tools

- Which tools you used, for what (e.g. *drafting the pagination loop in `src/download.py`*).
- What you checked (row counts, units, CRS, every line in `src/`).
- What is entirely yours (question, analysis choices, text).

## Licence

Code: see `LICENSE`. 
Data: see the licences in the table above.