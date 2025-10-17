import re
import pandas as pd
from io import StringIO


def to_num(x):
    if isinstance(x, str):
        x = re.sub(r'[^0-9.\-]', '', x)
    try:
        return float(x)
    except:
        return None

def clean_mining_csv(file_path: str) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    raw_fixed = re.sub(r'"\s*\n\s*', ' ', raw)
    raw_fixed = raw_fixed.replace('"', '')
    raw_fixed = re.sub(r'[ \t]+', ' ', raw_fixed)
    df = pd.read_csv(StringIO(raw_fixed), sep='|')

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    for col in ['Hashrate', 'Price', 'Revenue 24h', 'Profit 24h']:
        if col in df.columns:
            df[col + '_num'] = df[col].apply(to_num)

    return df

def clean_gpu_details_csv(file_path: str) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    raw_fixed = re.sub(r'"\s*\n\s*', ' ', raw)
    raw_fixed = raw_fixed.replace('"', '')
    raw_fixed = re.sub(r'[ \t]+', ' ', raw_fixed)
    df = pd.read_csv(StringIO(raw_fixed), sep='|')
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip().replace({'': None})
    return df

def clean_gpu_ai_specs_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df['GPU Name'] = df['GPU Name'].apply(clean_gpu_name)
    df['Speedup'] = df['Speedup'].apply(to_num)
    return df

def clean_gpu_name(name: str) -> str:
    remove_words = ['LambdaCloud', '1x']
    if pd.isna(name):
        return None
    name = name.lower()
    pattern = r'\b(?:' + '|'.join(remove_words) + r')\b'
    name = re.sub(pattern, '', name)
    name = re.sub(r'[^a-z0-9 ]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name
