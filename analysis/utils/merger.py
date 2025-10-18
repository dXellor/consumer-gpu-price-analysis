import pandas as pd
import re
from rapidfuzz import process, fuzz


def normalize_name(name: str) -> str:
    if pd.isna(name): 
        return None
    name = name.lower()
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    return re.sub(r"\s+", " ", name).strip()



def fuzzy_search_name(name: str, gpu_names: list):
    if pd.isna(name): return None, None
    match = process.extractOne(name, gpu_names, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= 80:
        return match[0], match[1]
    return None, None


def fuzzy_merge(df_mining: pd.DataFrame, df_gpu: pd.DataFrame) -> pd.DataFrame:

    df_mining["Model_clean"] = df_mining["Model"].apply(normalize_name)
    df_gpu["Product_Name_clean"] = df_gpu["Product Name"].apply(normalize_name)

    gpu_names = df_gpu["Product_Name_clean"].dropna().unique().tolist()

    matches = df_mining["Model_clean"].apply(lambda name: fuzzy_search_name(name, gpu_names))
    df_mining["Matched_Product_Name"] = [m[0] for m in matches]
    df_mining["fuzzy_score"] = [m[1] for m in matches]

    merged = df_mining.merge(
        df_gpu, left_on="Matched_Product_Name", right_on="Product_Name_clean", how="left"
    )
    merged = merged[(merged["fuzzy_score"] >= 80)]

    return merged

