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


INDICATORS_URL = "https://analisi.transparenciacatalunya.cat/resource/j7xc-3kfh.json"


def download_indicators(start, end):
    """Monthly Catalan energy indicators (GWh): net electricity exchange balance and demand."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"indicators_{start}_{end}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    params = {
        "$select": "data,cdeebc_saldointercanvielectr,cdeebc_demandaelectr",
        "$where": f"data >= '{start}T00:00:00' AND data <= '{end}T23:59:59'",
        "$order": "data", "$limit": 5000,
    }
    resp = requests.get(INDICATORS_URL, params=params, timeout=60)
    resp.raise_for_status()
    raw = pd.DataFrame(resp.json())
    out = pd.DataFrame({
        "date": pd.to_datetime(raw["data"]),
        "net_imports_gwh": pd.to_numeric(raw["cdeebc_saldointercanvielectr"]),
        "demand_gwh": pd.to_numeric(raw["cdeebc_demandaelectr"]),
    })
    out.to_csv(cache, index=False)
    return out


INE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{table}"
# INE table 50905: monthly national CPI by subclass (base 2021), 2002-2025.
# (Table 50937 in the brief is the annual version of the same data.)
CPI_BASE = {
    "olive_oil": "Nacional. Aceite de oliva",
    "fresh_fruit": "Nacional. Frutas frescas o refrigeradas",
    "fresh_vegetables": ("Nacional. Legumbres y hortalizas frescas o refrigeradas, "
                         "excepto patatas y otros tubérculos"),
    "general": "Nacional. Índice general",
}


def download_cpi(table=50905, nult=400):
    """Monthly CPI index and annual change (%) for the series in CPI_BASE (INE)."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"cpi_{table}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    resp = requests.get(INE_URL.format(table=table), params={"nult": nult}, timeout=180)
    resp.raise_for_status()
    series = {s["Nombre"].strip(): s["Data"] for s in resp.json()}
    cols = {}
    for key, base in CPI_BASE.items():
        for suffix, label in (("Índice.", "index"), ("Variación anual.", "yoy")):
            name = f"{base}. {suffix}"
            if name not in series:
                raise KeyError(f"series not found in table {table}: {name}")
            dates = pd.to_datetime([p["Fecha"] for p in series[name]], unit="ms", utc=True)
            dates = dates.tz_convert("Europe/Madrid").tz_localize(None)
            dates = dates.to_period("M").to_timestamp()
            cols[f"{key}_{label}"] = pd.Series([p["Valor"] for p in series[name]], index=dates)
    out = pd.DataFrame(cols).sort_index().rename_axis("date").reset_index()
    out.to_csv(cache, index=False)
    return out


OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"


def download_rain_openmeteo(name, lat, lon, start, end):
    """Daily precipitation (mm) of one grid point from Open-Meteo (reanalysis, no key)."""
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"rain_openmeteo_{name}_{start}_{end}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["date"])

    params = {"latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
              "daily": "precipitation_sum", "timezone": "Europe/Madrid"}
    resp = requests.get(OPENMETEO_URL, params=params, timeout=90)
    resp.raise_for_status()
    daily = resp.json()["daily"]
    out = pd.DataFrame({"date": pd.to_datetime(daily["time"]),
                        "value": daily["precipitation_sum"]})
    out.to_csv(cache, index=False)
    return out
