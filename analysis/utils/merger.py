import pandas as pd
from rapidfuzz import process, fuzz

def fuzzy_merge(df_mining: pd.DataFrame, df_gpu: pd.DataFrame, threshold=85) -> pd.DataFrame:
    df_mining = df_mining.copy()
    df_gpu = df_gpu.copy()

    df_gpu['Hashrate'] = pd.NA
    df_gpu['Revenue 24h'] = pd.NA

    gpu_names = df_gpu["Product Name"].tolist()

    for _, mining_row in df_mining.iterrows():
        mining_name = mining_row["Model"]
        
        best_match = process.extractOne(
            mining_name, 
            gpu_names, 
            scorer=fuzz.ratio
        )
    
        if best_match:
            _, score, index = best_match
            if score >= threshold:
                df_gpu.at[index, 'Hashrate'] = mining_row['Hashrate']
                df_gpu.at[index, 'Revenue 24h'] = mining_row['Revenue 24h']
                #print(df_gpu.info())
    df_gpu['Hashrate'] = pd.to_numeric(df_gpu['Hashrate'], errors='coerce')
    df_gpu['Revenue 24h'] = pd.to_numeric(df_gpu['Revenue 24h'], errors='coerce')
    return df_gpu

