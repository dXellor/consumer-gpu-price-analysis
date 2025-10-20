import pandas as pd
import re


def extract_number(value):
    if pd.isna(value):
        return None
    match = re.search(r'[\d.]+', str(value))
    return float(match.group()) if match else None


def extract_int(value):
    n = extract_number(value)
    if n is not None:
        return int(n)
    else:
        return None
    
def to_num(x):
    if isinstance(x, str):
        x = re.sub(r'[^0-9.\-]', '', x)
    try:
        return float(x)
    except:
        return None


def clean_currency(value):
    if pd.isna(value):
        return None
    cleaned = re.sub(r'[^0-9\.\-]', '', str(value))
    try:
        return float(cleaned)
    except ValueError:
        return None
    

def clean_gpu_name(name: str) -> str:
    remove_words = ['LambdaCloud', '1x']
    if pd.isna(name):
        return None
    name = name.lower()
    pattern = r'\b(?:' + '|'.join(remove_words) + r')\b'
    name = re.sub(pattern, '', name)
    name = re.sub(r'[^a-z0-9 ]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    name = re.sub(r"\b(LHR|FULL\s*UNLOCK|ENGINEERING SAMPLE)\b", "", name, flags=re.IGNORECASE)
    name = name.strip()
    return name


def format_date(value):
    if pd.isna(value):
        return None        
    try:
        dt = pd.to_datetime(value, errors='coerce')
        if pd.isna(dt):
            return value
        return dt.strftime("%b %Y")
    except Exception:
        return None


def mb_to_kb(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    match_mb = re.match(r'([\d\.]+)\s*MB', s, re.I)
    if match_mb:
        return float(match_mb[1]) * 1024

    match_kb = re.match(r'([\d\.]+)\s*KB', s, re.I)
    if match_kb:
        return float(match_kb[1])
    
    return None


def gb_to_mb(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    match_mb = re.match(r'([\d\.]+)\s*MB', s, re.I)
    if match_mb:
        return float(match_mb[1])
    match = re.match(r'([\d\.]+)\s*GB', str(value), re.I)
    if match:
        return float(match[1]) * 1024
    return None


def tb_to_gb(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    match_gb = re.match(r'([\d\.]+)\s*GB/s', s, re.I)
    if match_gb:
        return float(match_gb[1])
    match = re.match(r'([\d\.]+)\s*TB/s', str(value), re.I)
    if match:
        return float(match[1]) * 1024
    return None


def tf_to_gf(value):
    if pd.isna(value):
        return None
    s = str(value).replace(',', '').strip()

    match = re.match(r'([\d\.]+)\s*GFLOPS', s, re.I)
    if match:
        return float(match[1])
    match = re.match(r'([\d\.]+)\s*TFLOPS', str(value), re.I)
    if match:
        return float(match[1]) * 1000
    return value