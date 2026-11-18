"""Loader for the Idescat/DARP files produccions_comarcals_YYYY.(xls|xlsx).

Tested on the 2008 and 2025 files. Two layouts are handled:
  * old (2008): one header row starting with "CODI COMARCA", crop codes in the file
  * new (2025): 2-3 header rows with merged cells, comarca and group written only
    on the first row of each block, no codes (crop names only)
Every header that is not recognised is printed, never dropped silently.
Reading .xls files needs the package xlrd (pip install xlrd).
"""
import os
import re
import glob
import unicodedata
import pandas as pd


def _norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()


# ---------------------------------------------------------------- old layout
def _std_old(c):
    n = _norm(c)
    if "CODI COMARCA" in n:  return "comarca_code"
    if n == "COMARCA":       return "comarca"
    if "CODI CULTIU" in n:   return "crop_code"
    if n == "CONREU":        return "crop"
    if n.startswith("REND"):                       # yields first: one mentions ARBRES
        if "ARBRES" in n:    return "yield_trees_kg_tree"
        if "SECA" in n:      return "yield_dry_kg_ha"
        if "REG" in n:       return "yield_irr_kg_ha"
    if n.startswith("SUPERFICIE"):
        if "SECA" in n:      return "area_dry_ha"
        if "REG" in n:       return "area_irr_ha"
    if n.startswith("ARBRES DISSEMINATS") and "UNITATS" in n:
        return "trees_n"
    if n.startswith("PRODUCCIO"):
        return "production_t"
    return None


def _load_old(raw, hdr, year, sheet):
    df = raw.iloc[hdr + 1:].copy()
    cols = {}
    for j, c in enumerate(raw.iloc[hdr]):
        s = _std_old(c)
        if s is None:
            print(f"[{year}] sheet {sheet!r}: unrecognised column {c!r}")
        else:
            cols[j] = s
    df = df[list(cols)].rename(columns=cols)
    df["comarca_code"] = pd.to_numeric(df["comarca_code"], errors="coerce")
    df = df.dropna(subset=["comarca_code", "crop_code"])            # drops footnote rows
    df["group_code"] = (pd.to_numeric(df["crop_code"]) // 100).astype("Int64")
    return df


# ---------------------------------------------------------------- new layout
def _std_new(n):
    if n == "COMARCA":              return "comarca"
    if n.startswith("GRUP"):        return "group"
    if n in ("CONREU", "CULTIU"):   return "crop"
    if "PRODUCCIO" in n:            return "production_t"   # (2009: label inherited a span prefix)
    if "ARBRES DISSEMINATS" in n:                    # scattered trees (woody sheet)
        return "yield_trees_kg_tree" if "KG/ARBRE" in n else "trees_n"
    # measure: by prefix (2015+) or by unit when the header has none (2009)
    if n.startswith("SUPERFICIE") or n.endswith("(HA)"):
        stem, suf = "area", "_ha"
    elif n.startswith("RENDIMENT") or n.endswith("(KG/HA)"):
        stem, suf = "yield", "_kg_ha"
    else:
        return None
    if re.search(r"\bSECA\b", n):
        return f"{stem}_dry{suf}"
    if "REGADIU" in n:
        if "AIRE LLIURE" in n: return f"{stem}_irr_open{suf}"
        if "PROTEGIT" in n:    return f"{stem}_irr_protected{suf}"
        return f"{stem}_irr{suf}"
    return None


def _load_new(raw, hdr, year, sheet):
    # data start = first row after the header with at least 3 numeric cells
    # (2012: rows of zeros/dashes have <3 numbers, so first look for the first row with a crop name)
    crop_col = next((j for j in raw.columns if _norm(raw.iloc[hdr, j]) in ("CONREU", "CULTIU")), None)
    below = raw.iloc[hdr + 1:]
    if crop_col is not None and below[crop_col].notna().any():
        start = below[crop_col].first_valid_index()
    else:
        num = below.apply(pd.to_numeric, errors="coerce").notna().sum(axis=1)
        start = num[num >= 3].index[0]
    top = hdr - 1 if hdr > 0 and raw.iloc[hdr - 1].notna().sum() >= 2 else hdr   # 2009: labels sit one row above
    H = raw.iloc[top:start].astype(object).copy()    # object: ffill may put text in an all-empty (float) column
    span = H.iloc[0].notna().cumsum()                 # a merged cell = one span of columns
    H.iloc[0] = H.iloc[0].ffill()
    for r in range(1, len(H)):                        # fill sub-headers inside each span only
        H.iloc[r] = H.iloc[r].groupby(span).ffill()
    names = {}
    for j in H.columns:
        parts = [str(v) for v in H[j] if pd.notna(v)]
        names[j] = _norm(" ".join(parts))
    cols = {}
    for j, n in names.items():
        s = _std_new(n)
        if s is None:
            print(f"[{year}] sheet {sheet!r}: unrecognised column {n!r}")
        elif s in cols.values():                      # a merged label spilling over an empty column
            continue
        else:
            cols[j] = s
    df = raw.iloc[start:][list(cols)].rename(columns=cols)
    df["comarca"] = df["comarca"].ffill()             # written only on the first row of a block
    df["group"] = df["group"].ffill()
    return df.dropna(subset=["crop"])


# -------------------------------------------------------------------- common
# spellings found in the files -> one name per comarca
_COMARCA_FIX = {
    "BAIX EBRE": "Baix Ebre", "BAIXCAMP": "Baix Camp", "MARRESME": "Maresme",
    "GIRONES": "Gironès", "SELVA": "La Selva", "LA SELVA": "La Selva",
    "PLA D 'URGELL": "Pla d'Urgell", "RIBERA D'EBRRE": "Ribera d'Ebre",
    "TERA ALTA": "Terra Alta", "CONCA DE BARBERA": "Conca de Barberà",
    "ARAN": "Aran", "VALL D'ARAN": "Aran",
}


def fix_comarca(name):
    if pd.isna(name):
        return name
    n = re.sub(r"\s+", " ", str(name)).strip()
    return _COMARCA_FIX.get(_norm(n), n)



_PAIRS = [("area_dry_ha", "yield_dry_kg_ha"), ("area_irr_ha", "yield_irr_kg_ha"),
          ("area_irr_open_ha", "yield_irr_open_kg_ha"),
          ("area_irr_protected_ha", "yield_irr_protected_kg_ha")]


def _finish(df):
    """Masks yields where there is no area and adds comparable totals."""
    for a, y in _PAIRS:
        if a in df and y in df:
            df.loc[~(df[a] > 0), y] = pd.NA
    irr = [c for c in ("area_irr_ha", "area_irr_open_ha", "area_irr_protected_ha") if c in df]
    df["area_irr_total_ha"] = df[irr].sum(axis=1, min_count=1)
    df["area_total_ha"] = df["area_dry_ha"].fillna(0) + df["area_irr_total_ha"].fillna(0)
    prod = sum(df[a].fillna(0) * df[y].fillna(0) for a, y in _PAIRS if a in df and y in df)
    # area-weighted yield over the harvested area (excludes scattered trees)
    df["yield_total_kg_ha"] = (prod / df["area_total_ha"]).where(df["area_total_ha"] > 0)
    # yield from the reported production (differs from the above in a few rows of 2025)
    df["yield_prod_kg_ha"] = (df["production_t"] * 1000 / df["area_total_ha"]).where(df["area_total_ha"] > 0)
    return df


def load_year(path, year=None):
    """One tidy table for one file: one row per comarca x crop."""
    if year is None:
        year = int(re.search(r"(\d{4})", os.path.basename(path)).group(1))
    xl = pd.ExcelFile(path)
    parts = []
    for sheet in xl.sheet_names:
        if _norm(sheet).startswith("NOTA"):
            continue
        raw = pd.read_excel(xl, sheet, header=None)
        if raw.empty:
            continue
        hdr = next((i for i in range(len(raw))
                    if _norm(raw.iloc[i, 0]) in ("CODI COMARCA", "COMARCA")), None)
        if hdr is None:
            print(f"[{year}] sheet {sheet!r}: header row not found, skipped")
            continue
        old = _norm(raw.iloc[hdr, 0]) == "CODI COMARCA"
        df = (_load_old if old else _load_new)(raw, hdr, year, sheet)
        for c in df.columns.difference(["comarca", "crop", "group"]):
            df[c] = pd.to_numeric(df[c], errors="coerce")           # "-" becomes NaN
        for c in ("comarca", "crop", "group"):
            if c in df:
                df[c] = df[c].astype(str).str.strip().replace("nan", pd.NA)
        df["comarca"] = df["comarca"].map(fix_comarca)
        # True on the 2nd+ appearance of the same comarca/group/crop in a sheet
        # (the 2015 file lists one comarca twice with different numbers)
        key = [c for c in ("comarca", "group", "crop", "crop_code") if c in df]
        df["repeated"] = df.duplicated(key)
        df["sheet"] = _norm(sheet).lower()
        df["year"] = year
        parts.append(df)
    return _finish(pd.concat(parts, ignore_index=True))


def load_all(path="."):
    """path = a folder, a single file, or a glob pattern."""
    if os.path.isdir(path):
        files = sorted(os.path.join(path, f) for f in os.listdir(path)
                       if re.fullmatch(r"produccions_comarcals_\d{4}\.xlsx?", f, re.I))
    else:
        files = sorted(glob.glob(path))
    if not files:
        raise FileNotFoundError(f"No files found for {path!r} (current folder: {os.getcwd()})")
    print("Loading:", [os.path.basename(f) for f in files])
    frames, failed = [], []
    for f in files:
        try:
            frames.append(load_year(f))
        except Exception as e:                       # keep going, report at the end
            failed.append((os.path.basename(f), repr(e)))
    if failed:
        print("FAILED files:")
        for name, err in failed:
            print("  ", name, "->", err)
    if not frames:
        raise RuntimeError("No file could be loaded")
    return pd.concat(frames, ignore_index=True)


# ----------------------------------------------------- harmonised crop series
def crop_group(name):
    """Name that is comparable across 2008-2025 (wheat/barley/olive variants merged)."""
    if pd.isna(name):
        return name
    n = re.sub(r"\([^)]*\)", "", str(name))                 # (nou conreu), (fins 2016), ...
    n = re.sub(r"\s+", " ", n).strip()
    k = _norm(n)
    if k.startswith("BLAT DE MORO"):
        return "Blat de moro farratger" if "FARRATGER" in k else "Blat de moro"
    if k.startswith("BLAT"):   return "Blat"                # tou + dur + khorasan (before 2017 one 'Blat')
    if k.startswith("ORDI"):   return "Ordi"                # 2 and 6 rows, winter
    if k.startswith("OLIVERA"):return "Olivera"             # oil + table + dual purpose
    if k.startswith("AMETLLA"):return "Ametller"            # 2016-2018 'Ametlla (closca)' = almond tree
    if k.startswith("AVELLANA"):return "Avellaner"          # 2016-2018 'Avellana (closca)'
    if k.startswith("NOU") and "CLOSCA" in _norm(str(name)):
        return "Noguera"                                    # 2016-2018 'Nou (closca)'
    return n


def harmonise(df, drop_repeated=True):
    """Sums the variants that share crop_group() and recomputes yields from the production."""
    d = df[~df["repeated"]] if drop_repeated else df
    d = d.assign(crop_h=d["crop"].map(crop_group))
    g = d.groupby(["year", "comarca", "crop_h"], as_index=False)[
        ["area_dry_ha", "area_irr_total_ha", "area_total_ha", "production_t"]].sum(min_count=1)
    g["yield_prod_kg_ha"] = (g["production_t"] * 1000 / g["area_total_ha"]).where(g["area_total_ha"] > 0)
    return g