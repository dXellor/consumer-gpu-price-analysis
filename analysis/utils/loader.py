import pandas as pd
from pathlib import Path
from utils.cleaner import clean_mining_csv, clean_gpu_details_csv, clean_gpu_ai_specs_csv

DATA_DIR = Path("D:/Fax/I semestar/Sistemi za istraživanje i analizu podataka/Projekat/consumer-gpu-price-analysis/data")

def load_ai_trends() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "ai-trends-weekly.csv", parse_dates=["Week"])
    df = df.rename(columns={"ai training": "ai_training"})
    return df

#monero_2023-08-01..., ethereum-classic_2023-08-01...
def load_crypto_prices(crypto_name: str) -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/{crypto_name}_2023-08-01_2025-08-01.csv", parse_dates=["End"])
    df = df[["End", "Close"]]
    df = df.rename(columns={"End": "Date"})
    return df

def load_gpu_details() -> pd.DataFrame:
    init_df = clean_gpu_details_csv(f"{DATA_DIR}/gpu-details.csv")
    return init_df
    

def load_gpu_ai_specs() -> pd.DataFrame:
    return clean_gpu_ai_specs_csv(f"{DATA_DIR}/gpu-ai-specs-lambda.csv")

#mining-gpus-...
def load_mining_data(crypto_file_name: str) -> pd.DataFrame:
    init_df = clean_mining_csv(f"{DATA_DIR}/mining-gpus-{crypto_file_name}.csv")
    return init_df[['Model', 'Release Date', 'Hashrate']]
