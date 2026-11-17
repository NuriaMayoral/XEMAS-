"""Loaders for the Open Data BCN datasets used in idea 2 (heat inequality in Barcelona).

Every download is cached in data/raw/. Section ids are district * 1000 + section
(for example 1001 = district 1, section 1), the format used by the population register.
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely import wkt

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
CKAN = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show"
CRS = "EPSG:25831"  # ETRS89 / UTM zone 31N (metres)


def _download(package, resource_name):
    """Download one resource of an Open Data BCN dataset (cached in data/raw/)."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"bcn_{package}_{resource_name}"
    if not path.exists():
        info = requests.get(CKAN, params={"id": package}, timeout=60)
        info.raise_for_status()
        urls = {r["name"]: r["url"] for r in info.json()["result"]["resources"]}
        if resource_name not in urls:
            raise KeyError(f"{resource_name} not found in {package}: {sorted(urls)[:5]}...")
        data = requests.get(urls[resource_name], timeout=120)
        data.raise_for_status()
        path.write_bytes(data.content)
    return path


def download_income(year=2023):
    """Disposable income of households per person (EUR) by census section."""
    path = _download("renda-disponible-llars-bcn", f"{year}_renda_disponible_llars_per_persona.csv")
    raw = pd.read_csv(path)
    return pd.DataFrame({
        "section_id": raw["Codi_Districte"] * 1000 + raw["Seccio_Censal"],
        "district": raw["Nom_Districte"],
        "neighbourhood": raw["Nom_Barri"],
        "income_eur": raw["Import_Euros"],
    })


def download_population(year=2024):
    """Population by census section on 1 January of `year` (municipal register)."""
    path = _download("pad_mdbas_sexe", f"{year}_pad_mdbas_sexe.csv")
    raw = pd.read_csv(path)
    out = raw.groupby("Seccio_Censal")["Valor"].sum()
    return out.rename_axis("section_id").rename("population").reset_index()


def download_sections():
    """Census section polygons (EPSG:25831)."""
    path = _download("20170706-districtes-barris", "BarcelonaCiutat_SeccionsCensals.csv")
    raw = pd.read_csv(path)
    geometry = raw["geometria_etrs89"].map(wkt.loads)
    out = gpd.GeoDataFrame(
        {"section_id": raw["codi_districte"] * 1000 + raw["codi_seccio_censal"]},
        geometry=geometry, crs=CRS,
    )
    if not out.geometry.is_valid.all():
        out["geometry"] = out.geometry.make_valid()
    return out


def download_shelters():
    """Climate shelters network (points, EPSG:25831). The CSV is encoded in UTF-16."""
    path = _download("xarxa-refugis-climatics",
                     "opendatabcn_NP-NASIA_xarxa-refugis-climatics-csv.csv")
    raw = pd.read_csv(path, encoding="utf-16", low_memory=False)
    raw.columns = [c.strip().lstrip("﻿") for c in raw.columns]
    return gpd.GeoDataFrame(
        {
            "register_id": raw["register_id"].astype(str).str.lstrip("﻿"),
            "name": raw["name"],
            "institution": raw["institution_name"],
            "district": raw["addresses_district_name"],
            "neighbourhood": raw["addresses_neighborhood_name"],
        },
        geometry=gpd.points_from_xy(raw["geo_epgs_25831_x"], raw["geo_epgs_25831_y"]),
        crs=CRS,
    )


def download_population_age(year=2024):
    """Population aged 75 or more and aged 0-4 by census section (1 January of `year`).

    Counts below the statistical secrecy threshold are published as '..' and are counted
    as 0 here (about 0.1% of the population is lost).
    """
    path = _download("pad_mdbas_edat-q", f"{year}_pad_mdbas_edat-q.csv")
    raw = pd.read_csv(path, dtype={"Valor": str})
    raw["Valor"] = pd.to_numeric(raw["Valor"], errors="coerce").fillna(0)
    old = raw[raw["EDAT_Q"] >= 15].groupby("Seccio_Censal")["Valor"].sum().rename("pop_75plus")
    young = raw[raw["EDAT_Q"] == 0].groupby("Seccio_Censal")["Valor"].sum().rename("pop_0_4")
    return pd.concat([old, young], axis=1).rename_axis("section_id").reset_index()


def download_heat_vulnerability():
    """Global vulnerability to heat by area (municipal study of the 2015 heat wave).

    Polygons in EPSG:25831 with one column, `vuln_total` (integer score from 2 to 9). The
    documentation of the file is minimal: higher values go with lower-income areas and with
    the poorest hillside sections, so they are read as higher vulnerability.
    """
    path = _download("factor-de-vulnerabilitat", "2015_vulnera_global.gpkg")
    return gpd.read_file(path).rename(columns={"VulnTot_On": "vuln_total"})
