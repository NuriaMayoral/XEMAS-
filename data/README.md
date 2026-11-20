# Data

Everything the notebooks need is in this folder, so they run offline. Files written by the notebooks go to `../figures/`, never here.

## Files

| Path | What | Source | Licence / terms | Retrieved | Used in |
|---|---|---|---|---|---|
| `Incendis_forestals_a_Catalunya__Anys_2011-2024_20261116.csv` | Forest fires in Catalonia, one row per fire, 2011-2024 (7,545 rows): date, comarca, municipality and hectares burned (tree-covered, non-tree forest, non-forest, total forest) | [Transparència Catalunya `bks7-dkfd`](https://analisi.transparenciacatalunya.cat/Medi-Rural-Pesca/Incendis-forestals-a-Catalunya-Anys-2011-2024/bks7-dkfd/about_data) | Portal terms of use (attribution) | 2026-11-16 | map_fires_municipalities |
| `divisions-administratives-v2r1-municipis-1000000-20250730.json` | Municipality outlines of Catalonia (1:1,000,000), EPSG:4326 | [ICGC, Divisions administratives v2r1 (2025-07-30)](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) | ICGC terms of use (attribution) | 2025-07-30 | map_fires_municipalities |
| `divisions-administratives-v2r1-comarques-250000-20250730.json` | Comarca outlines of Catalonia (1:250,000), EPSG:4326 | same as above | same | 2025-07-30 | — |
| `Sequera_Catalunya.csv` | Drought status changes per municipality and exploitation unit, 2021-2025 (8,677 rows; hydrological and pluviometric status) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | Portal terms of use (attribution) | TODO | — |
| `Quantitat_d_aigua_als_embassaments_Catalunya.csv` | Daily water level, stored volume (hm3) and percentage of capacity in 9 reservoirs of the Catalan internal basins, 2000-2026 (88,308 rows) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | Portal terms of use (attribution) | TODO | — |
| `Aigües_subterrànies_de_Catalunya.csv` | Groundwater monitoring: water depth and piezometric level per station and date, with coordinates and municipality (244,538 rows) | [Transparència Catalunya `TODO`](https://analisi.transparenciacatalunya.cat/) | Portal terms of use (attribution) | TODO | — |

Notes:

- Numbers in the CSVs use a comma as decimal separator (and a dot for thousands in some columns), so read them with `decimal=","` and `thousands="."`.
- The municipality code in the fires CSV has no leading zero (e.g. `80018`); pad it to 6 digits before joining with the maps.

## Repositories of open datasets

### Open data portals

- [data.europa.eu](https://data.europa.eu/en) · [datos.gob.es](https://datos.gob.es/es/) · [INE](https://www.ine.es/) · [Eurostat](https://ec.europa.eu/eurostat)
- [Transparència Catalunya](https://analisi.transparenciacatalunya.cat/) · [Dades Obertes DIBA](https://dadesobertes.diba.cat/) · [Open Data BCN](https://opendata-ajuntament.barcelona.cat/es)