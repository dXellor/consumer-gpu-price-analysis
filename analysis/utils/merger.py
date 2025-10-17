import pandas as pd
import re
from datetime import datetime
from rapidfuzz import process, fuzz
from dateutil import parser


def normalize_name(name: str) -> str:
    if pd.isna(name): 
        return None
    name = name.lower()
    name = re.sub(r"(nvidia|amd|geforce|radeon|gpu|graphics|mobile|laptop)", "", name)
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def parse_date(date_str: str) -> datetime:
    if pd.isna(date_str): return None
    try: return parser.parse(str(date_str), fuzzy=True)
    except Exception:
        return datetime(int(re.search(r"\d{4}", str(date_str)).group()), 7, 1) if re.search(r"\d{4}", str(date_str)) else None


def fuzzy_search_name(name: str, gpu_names: list):
    if pd.isna(name): return None, None
    match = process.extractOne(name, gpu_names, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= 80:
        return match[0], match[1]
    return None, None


def date_close(d1: datetime, d2: datetime, days=60) -> bool:
    if pd.isna(d1) or pd.isna(d2): return True
    return abs((d1 - d2).days) <= days


def fuzzy_merge(df_mining: pd.DataFrame, df_gpu: pd.DataFrame) -> pd.DataFrame:

    df_mining["Model_clean"] = df_mining["Model"].apply(normalize_name)
    df_gpu["Product_Name_clean"] = df_gpu["Product Name"].apply(normalize_name)

    df_mining["Release_Date"] = df_mining["Release Date"].apply(parse_date)
    df_gpu["Release_Date"] = df_gpu["Release Date"].apply(parse_date)

    gpu_names = df_gpu["Product_Name_clean"].dropna().unique().tolist()

    matches = df_mining["Model_clean"].apply(lambda name: fuzzy_search_name(name, gpu_names))
    df_mining["Matched_Product_Name"] = [m[0] for m in matches]
    df_mining["fuzzy_score"] = [m[1] for m in matches]

    merged = df_mining.merge(
        df_gpu, left_on="Matched_Product_Name", right_on="Product_Name_clean", how="left"
    )

    # Compare release dates
    merged["Date_match"] = merged.apply(
        lambda r: date_close(r["Release_Date_x"], r["Release_Date_y"]), axis=1
    )

    # Filter by fuzzy score and date match
    merged = merged[(merged["fuzzy_score"] >= 80) & (merged["Date_match"])]

    return merged

