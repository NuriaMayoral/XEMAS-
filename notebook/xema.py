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
