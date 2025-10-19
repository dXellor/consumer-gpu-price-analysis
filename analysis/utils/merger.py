import pandas as pd
import re
from rapidfuzz import process, fuzz
from difflib import SequenceMatcher



def fuzzy_merge(df_mining: pd.DataFrame, df_gpu: pd.DataFrame, threshold=85) -> pd.DataFrame:
    df_mining = df_mining.copy()
    df_gpu = df_gpu.copy()

    # Prepare mining columns in GPU dataframe
    df_gpu['Hashrate'] = pd.NA  # Add more mining columns here if needed

    # Create a list of bigger GPU names
    gpu_names = df_gpu["Product Name"].tolist()

    # Iterate over smaller mining list
    for _, mining_row in df_mining.iterrows():
        mining_name = mining_row["Model"]
        # Find best match in bigger list
        
        best_match = process.extractOne(
            mining_name, 
            gpu_names, 
            scorer=fuzz.ratio
        )
        
        if best_match:
            matched_name, score, index = best_match
            if score >= threshold:
                df_gpu.at[index, 'Hashrate'] = mining_row['Hashrate']
                #print(df_gpu.info())
                # df_gpu.at[index, 'Tensor Cores'] = mining_row['Tensor Cores']
    return df_gpu

