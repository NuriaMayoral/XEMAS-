from pathlib import Path

import pandas as pd
import requests

URL = "https://analisi.transparenciacatalunya.cat/resource/7bvh-jvq2.json"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def download_daily(station, variable, start, end, page=50_000):
    """Daily XEMA series for one station and variable, cached in data/raw/."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"xema_{station}_{variable}_{start}_{end}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    where = (
        f"codi_estacio='{station}' AND codi_variable='{variable}' "
        f"AND data_lectura >= '{start}T00:00:00' "
        f"AND data_lectura <= '{end}T23:59:59'"
    )
    chunks, offset = [], 0
    while True:
        params = {"$where": where, "$order": "data_lectura",
                  "$limit": page, "$offset": offset}
        resp = requests.get(URL, params=params, timeout=60)
        resp.raise_for_status()
        rows = resp.json()
        chunks.append(pd.DataFrame(rows))
        if len(rows) < page:
            break
        offset += page

    raw = pd.concat(chunks, ignore_index=True)
    out = pd.DataFrame({
        "date": pd.to_datetime(raw["data_lectura"]),
        "value": pd.to_numeric(raw["valor"]),
    })
    out.to_csv(cache, index=False)
    return out


DEMAND_URL = "https://analisi.transparenciacatalunya.cat/resource/hx6q-ykhb.json"


def download_demand(start, end, page=50_000):
    """Daily electricity demand in Catalonia (MWh), cached in data/raw/."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"demand_{start}_{end}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    where = f"data >= '{start}T00:00:00' AND data <= '{end}T23:59:59'"
    chunks, offset = [], 0
    while True:
        params = {"$select": "data,total", "$where": where,
                  "$order": "data", "$limit": page, "$offset": offset}
        resp = requests.get(DEMAND_URL, params=params, timeout=60)
        resp.raise_for_status()
        rows = resp.json()
        chunks.append(pd.DataFrame(rows))
        if len(rows) < page:
            break
        offset += page

    raw = pd.concat(chunks, ignore_index=True)
    out = pd.DataFrame({
        "date": pd.to_datetime(raw["data"]),
        "demand_mwh": pd.to_numeric(raw["total"]),
    })
    out.to_csv(cache, index=False)
    return out


REDATA_URL = "https://apidatos.ree.es/es/datos/generacion/estructura-generacion"


def download_generation(start_year, end_year):
    """Monthly electricity generation in Catalonia by technology (MWh), REData."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"generation_{start_year}_{end_year}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    rows = []
    for year in range(start_year, end_year + 1):
        params = {
            "start_date": f"{year}-01-01T00:00", "end_date": f"{year}-12-31T23:59",
            "time_trunc": "month", "geo_trunc": "electric_system",
            "geo_limit": "ccaa", "geo_ids": 9,
        }
        resp = requests.get(REDATA_URL, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        if "included" not in payload:
            raise RuntimeError(f"REData {year}: {payload.get('errors')}")
        for series in payload["included"]:
            tech = series["attributes"]["title"]
            for v in series["attributes"]["values"]:
                rows.append({"date": v["datetime"][:10], "technology": tech,
                             "value_mwh": v["value"]})

    out = pd.DataFrame(rows)
    out["date"] = pd.to_datetime(out["date"])
    out.to_csv(cache, index=False)
    return out


RESERVOIR_URL = "https://analisi.transparenciacatalunya.cat/resource/gn9e-3qhr.json"


def download_reservoirs(start, end, page=50_000):
    """Daily volume of the 9 Conques Internes reservoirs, cached in data/raw/."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"reservoirs_{start}_{end}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    where = f"dia >= '{start}T00:00:00' AND dia <= '{end}T23:59:59'"
    chunks, offset = [], 0
    while True:
        params = {"$where": where, "$order": "dia, estaci",
                  "$limit": page, "$offset": offset}
        resp = requests.get(RESERVOIR_URL, params=params, timeout=60)
        resp.raise_for_status()
        rows = resp.json()
        chunks.append(pd.DataFrame(rows))
        if len(rows) < page:
            break
        offset += page

    raw = pd.concat(chunks, ignore_index=True)
    out = pd.DataFrame({
        "date": pd.to_datetime(raw["dia"]),
        "reservoir": raw["estaci"],
        "pct": pd.to_numeric(raw["percentatge_volum_embassat"]),
        "volume_hm3": pd.to_numeric(raw["volum_embassat"]),
    })
    out.to_csv(cache, index=False)
    return out
