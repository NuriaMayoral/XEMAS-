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

Notes:

- Numbers in the CSVs use a comma as decimal separator (and a dot for thousands in some columns), so read them with `decimal=","` and `thousands="."`.
- The municipality code in the fires CSV has no leading zero (e.g. `80018`); pad it to 6 digits before joining with the maps.

## Repositories of open datasets

### Open data portals

- [Transparència Catalunya](https://analisi.transparenciacatalunya.cat/) · [ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives)

- ## How to run

```console
git clone https://github.com/NuriaMayoral/XEMAS-.git
cd <XEMAS->
uv sync            # or: conda env create -f environment.yml
uv run jupyter lab
```
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

Code: see `LICENSE`. Data: see the licences in the table above.