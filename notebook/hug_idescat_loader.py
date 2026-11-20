"""This file is used as a function repository for the main jupiter notebook
The goal is to be able to load all data Idescat/DARP files 
produccions_comarcals_YYYY.(xls|xlsx) (see 
https://agricultura.gencat.cat/ca/departament/observatori-agroambiental/estadistiques/agricultura/estadistiques-definitives-conreus/). 
Because the data resides in diferent files and is structured diferently, we need 
a whole bunch of functions specially for loading the data, that's why we built a 
diferent script for this situation and to avoid oversaturating the main notebook.

There are two types of file, approx from 2008 to 2013, there is one header row starting 
with "CODI COMARCA" and crop codes in the file. The file document is all in lowercase 
and in .xls format. From 2013 to 2025, there are 2-3 header rows with merged cells, 
comarca and group written only on the first row of each block and no crop codes (names 
only). Also, crop name changes from 2023 onwards for some categories such as hazelnuts 
and almonds. 

The registering of data also changes from 2023 as for olives and wine, the location saved 
changes from the plantation location to the cellar location. We believe this hasn't affected 
much (at least the map plot doesn't seem much afected) as we have restricted the location to 
comarques/counties and the majority of cellars are located in the same comarca than the 
plantation.

In the data treatment part, every header that is not recognised is printed, never dropped 
silently.

Functions:
_norm(s)

"""
import os
import re
import glob
import unicodedata
import pandas as pd


def _norm(s):
    """Returns the data normalised into a standard form, these implies eliminating punctuation, 
    converting to uppercase and setting blank data to NaN (str). """

    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode() # NFKD splits letters with accents to the plain letter
    return re.sub(r"\s+", " ", s).strip().upper()                                # + the accent. Then the ASCII ignores whatever isn't a normal letter. 



def _std_old(c):
    """This functions is dedicated to the files from 2008 to 2013. 
    It will convert the messy naming
    of column headers into standard names. 
    By specific analysis of the files we have been able to compare general namings to the
    normalised ones and rename it to a common naming."""

    n = _norm(c)
    if "CODI COMARCA" in n:  return "comarca_code"
    if n == "COMARCA":       return "comarca"
    if "CODI CULTIU" in n:   return "crop_code"
    if n == "CONREU":        return "crop"
    if n.startswith("REND"): #rendiment
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
    """The data files have different layouts. 2008 file layout only includes 3 sheets. The first one is
    merely informative, while the second and third retrieve data. In the second, there's one row of headers , 
    while in the third there are 2 rows, merging all columns, without any relevant content)"""
    df = raw.iloc[hdr + 1:].copy() # we discount the header
    cols = {}
    for j, c in enumerate(raw.iloc[hdr]): # iterate over the column headers and recognize them with 
        s = _std_old(c)
        if s is None:
            print(f"[{year}] sheet {sheet!r}: unrecognised column {c!r}") # We don't delete without leaving a note
        else:
            cols[j] = s
    df = df[list(cols)].rename(columns=cols) # Saving of the corrected headers in the df
    df["comarca_code"] = pd.to_numeric(df["comarca_code"], errors="coerce")  # We convert the codes (comarca and crop)
    df = df.dropna(subset=["comarca_code", "crop_code"])# we drop footnote rows
    df["group_code"] = (pd.to_numeric(df["crop_code"]) // 100).astype("Int64")
    return df



def _std_new(n):
    """This functions is dedicated to the files from 2009 to 2025. It will convert the messy naming
    of column headers. By specific analysis of the files we have been able to compare general namings to the
    normalised ones and rename it to a common naming. We splitted files into old and new documents, as the 
    first have codi comarca and the latter do not"""

    if n == "COMARCA":              return "comarca"
    if n.startswith("GRUP"):        return "group"
    if n in ("CONREU", "CULTIU"):   return "crop"
    if "PRODUCCIO" in n:            return "production_t" # 2009 label inherited a span prefix. More format divergencees.
    if "ARBRES DISSEMINATS" in n: # scattered trees 
        return "yield_trees_kg_tree" if "KG/ARBRE" in n else "trees_n"
    if n.startswith("SUPERFICIE") or n.endswith("(HA)"): # We recover the surface units
        stem, suf = "area", "_ha"
    elif n.startswith("RENDIMENT") or n.endswith("(KG/HA)"): # We recover the performance units
        stem, suf = "yield", "_kg_ha"
    else:
        return None
    if re.search(r"\bSECA\b", n): # Now we further classificate into drylands or wetlands and add their units
        return f"{stem}_dry{suf}"
    if "REGADIU" in n:
        if "AIRE LLIURE" in n: return f"{stem}_irr_open{suf}"
        if "PROTEGIT" in n:    return f"{stem}_irr_protected{suf}"
        return f"{stem}_irr{suf}"
    return None


def _load_new(raw, hdr, year, sheet):
    """This function loads the data into df cleaning rough original format. The data files have different layouts. 
    From 2009 files, the layout includes 4 sheets. The first one is merely informative, while the rest retrieve data. 
    Except in the first, there're 2 or 3 rows of headers. There's also non data containing columns."""
    
    crop_col = next((j for j in raw.columns if _norm(raw.iloc[hdr, j]) in ("CONREU", "CULTIU")), None) # Find the first column with data
    below = raw.iloc[hdr + 1:]
    if crop_col is not None and below[crop_col].notna().any(): # Also locate the first row with data
        start = below[crop_col].first_valid_index()
    else:
        num = below.apply(pd.to_numeric, errors="coerce").notna().sum(axis=1)
        start = num[num >= 3].index[0]
    top = hdr - 1 if hdr > 0 and raw.iloc[hdr - 1].notna().sum() >= 2 else hdr # For 2009: labels sit one row above
    H = raw.iloc[top:start].astype(object).copy()    # object: ffill may put text in an all-empty (float) column
    span = H.iloc[0].notna().cumsum() # Understand merged cells. Assign a number to each cell (repeated if merged)
    H.iloc[0] = H.iloc[0].ffill() # Avoids that thew numbers in the spans overflows to other spans by filling in each
    for r in range(1, len(H)):# fill sub-headers inside each span only
        H.iloc[r] = H.iloc[r].groupby(span).ffill()
    names = {}
    for j in H.columns: # Naming of the columns by joining the non-empty headers through norm
        parts = [str(v) for v in H[j] if pd.notna(v)]
        names[j] = _norm(" ".join(parts))
    cols = {}
    for j, n in names.items(): # different rows may be also merged
        s = _std_new(n)
        if s is None:
            print(f"[{year}] sheet {sheet!r}: unrecognised column {n!r}")
        elif s in cols.values(): # a merged label spilling over an empty column
            continue
        else:
            cols[j] = s
    df = raw.iloc[start:][list(cols)].rename(columns=cols)
    df["comarca"] = df["comarca"].ffill() # written only on the first row of a block
    df["group"] = df["group"].ffill()
    return df.dropna(subset=["crop"])



# Fixing the error in names or double definitions
_COMARCA_FIX = {
    "BAIX EBRE": "Baix Ebre", "BAIXCAMP": "Baix Camp", "MARRESME": "Maresme",
    "GIRONES": "Gironès", "SELVA": "La Selva", "LA SELVA": "La Selva",
    "PLA D 'URGELL": "Pla d'Urgell", "RIBERA D'EBRRE": "Ribera d'Ebre",
    "TERA ALTA": "Terra Alta", "CONCA DE BARBERA": "Conca de Barberà",
    "ARAN": "Aran", "VALL D'ARAN": "Aran", "VAL D'ARAN": "Aran",
}


def fix_comarca(name): # Using the previous dictionary, fixes column headers
    if pd.isna(name):
        return name
    n = re.sub(r"\s+", " ", str(name)).strip()
    return _COMARCA_FIX.get(_norm(n), n)



_PAIRS = [("area_dry_ha", "yield_dry_kg_ha"), ("area_irr_ha", "yield_irr_kg_ha"),
          ("area_irr_open_ha", "yield_irr_open_kg_ha"),
          ("area_irr_protected_ha", "yield_irr_protected_kg_ha")]


def _finish(df):
    """This function takes the area, yield and production columns of one year and cleans them. It then builds 
    the totals that the rest of functions uses"""
    for a, y in _PAIRS: # Take one vector and it's components (area, yield)
        if a in df and y in df:
            df.loc[~(df[a] > 0), y] = pd.NA # Blanks yield that have no area (some error have been found in the original data in this sense)
    irr = [c for c in ("area_irr_ha", "area_irr_open_ha", "area_irr_protected_ha") if c in df] # adss all irrigated area (open and protected)
    df["area_irr_total_ha"] = df[irr].sum(axis=1, min_count=1)
    df["area_total_ha"] = df["area_dry_ha"].fillna(0) + df["area_irr_total_ha"].fillna(0) # adds all area (irrigated and dry)
    prod = sum(df[a].fillna(0) * df[y].fillna(0) for a, y in _PAIRS if a in df and y in df)
    # area-weighted yield over the harvested area (excludes scattered trees)
    df["yield_total_kg_ha"] = (prod / df["area_total_ha"]).where(df["area_total_ha"] > 0)
    # yield from the reported production (differs from the above in a few rows of 2025)
    df["yield_prod_kg_ha"] = (df["production_t"] * 1000 / df["area_total_ha"]).where(df["area_total_ha"] > 0)
    return df


def load_year(path, year=None):
    """This function uses the previous load functions to retrieve a df per year: one row per comarca x crop."""
    if year is None:
        year = int(re.search(r"(\d{4})", os.path.basename(path)).group(1)) # take the file of that year
    xl = pd.ExcelFile(path)
    parts = []
    for sheet in xl.sheet_names: 
        if _norm(sheet).startswith("NOTA"): # Avoid first sheet if it's like a readme
            continue
        raw = pd.read_excel(xl, sheet, header=None)
        if raw.empty:
            continue
        hdr = next((i for i in range(len(raw)) # Identify the headers and normalise them
                    if _norm(raw.iloc[i, 0]) in ("CODI COMARCA", "COMARCA")), None)
        if hdr is None:
            print(f"[{year}] sheet {sheet!r}: header row not found, skipped") # skipped but leaving a note
            continue
        old = _norm(raw.iloc[hdr, 0]) == "CODI COMARCA" # Old format corresponding to 2008 is the only having CODI COMARCA first
        df = (_load_old if old else _load_new)(raw, hdr, year, sheet) # if locates this first cell, uses load_old function, otherwise load_new
        for c in df.columns.difference(["comarca", "crop", "group"]): # Except this ones, all columns become numbers
            df[c] = pd.to_numeric(df[c], errors="coerce") # "-" becomes NaN
        for c in ("comarca", "crop", "group"): # Then this assure are strings
            if c in df: 
                df[c] = df[c].astype(str).str.strip().replace("nan", pd.NA)
        df["comarca"] = df["comarca"].map(fix_comarca) 
        # TO avoid having twice a Comarca (as in 2015)
        key = [c for c in ("comarca", "group", "crop", "crop_code") if c in df]
        df["repeated"] = df.duplicated(key)
        df["sheet"] = _norm(sheet).lower()
        df["year"] = year
        parts.append(df)
    return _finish(pd.concat(parts, ignore_index=True))


def load_all(path="."):
    """This function loads all files and merge them. Uses all the previous loading functions"""
    if os.path.isdir(path): # If the path is a folder, identifies all the files; otherwise the path is a single file
        files = sorted(os.path.join(path, f) for f in os.listdir(path)
                       if re.fullmatch(r"produccions_comarcals_\d{4}\.xlsx?", f, re.I))
    else:
        files = sorted(glob.glob(path))
    if not files: # if there's no files
        raise FileNotFoundError(f"No files found for {path!r} (current folder: {os.getcwd()})")
    print("Loading:", [os.path.basename(f) for f in files]) # To keep track of what are you loading
    frames, failed = [], []
    for f in files: # load the files
        try:
            frames.append(load_year(f)) 
        except Exception as e: # keep going, report at the end
            failed.append((os.path.basename(f), repr(e)))
    if failed:
        print("FAILED files:")
        for name, err in failed:
            print("  ", name, "->", err)
    if not frames:
        raise RuntimeError("No file could be loaded")
    return pd.concat(frames, ignore_index=True)



def crop_group(name):
    """This function unifies the name of the crops that are different across 2008-2025 (wheat/barley/olive 
    variants merged and different names for the same product)."""
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
    """This function sums the variants that share crop_group() and recomputes yields from the production."""
    d = df[~df["repeated"]] if drop_repeated else df # eliminate repetitions
    d = d.assign(crop_h=d["crop"].map(crop_group)) # unify crop name 
    g = d.groupby(["year", "comarca", "crop_h"], as_index=False)[
        ["area_dry_ha", "area_irr_total_ha", "area_total_ha", "production_t"]].sum(min_count=1) # sum variants 
    g["yield_prod_kg_ha"] = (g["production_t"] * 1000 / g["area_total_ha"]).where(g["area_total_ha"] > 0)
    return g