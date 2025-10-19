import re
import pandas as pd
from io import StringIO
import utils.helpers as helpers


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

def clean_mining_csv(file_path: str) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    raw_fixed = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace('\n', ' '), raw)
    raw_fixed = raw_fixed.replace('"', '')
    raw_fixed = re.sub(r'RandomX\s*·\s*', '', raw_fixed, flags=re.IGNORECASE)
    raw_fixed = re.sub(r'[ \t]+', ' ', raw_fixed)
    df = pd.read_csv(StringIO(raw_fixed), sep='|')

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    df['Model'] = df['Model'].apply(clean_gpu_name)
    df = df.drop_duplicates(subset=["Model"], keep="first")
    print(len(df['Model']))
    
    df['Hashrate'] = df['Hashrate'].str.replace(
        r'(\d+(?:\.\d+)?)\s*[kK]\s*h/s',
        lambda m: str(float(m.group(1)) * 1000) + ' h/s',
        regex=True
    )

    df['Hashrate'] = df['Hashrate'].str.replace(
        r'(\d+(?:\.\d+)?)\s*[mM]\s*h/s',
        lambda m: str(float(m.group(1)) * 1000000) + ' h/s',
        regex=True
    )

    df['Hashrate'] = df['Hashrate'].str.replace('h/s', '', regex=False).str.strip()
    df['Hashrate'] = df['Hashrate'].str.split().str[0]
    df['Hashrate'] = df['Hashrate'].apply(to_num)
    df['Revenue 24h'] = df['Revenue 24h'].apply(clean_currency)

    return df[['Model', 'Release Date', 'Hashrate', 'Revenue 24h']]


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

def format_date(value):
    if pd.isna(value):
        return None
    # Remove "th", "st", "nd", "rd" suffixes
    
    value = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(value))
    
    try:
        dt = pd.to_datetime(value, errors='coerce')
        if pd.isna(dt):
            return value
        return dt.strftime("%b %Y")  # Format: Oct 2010
    except Exception:
        return None
        
def clean_gpu_details_csv(file_path: str) -> pd.DataFrame:
    relevant_columns = [
    "Product Name", "Release Date",
    "Base Clock", "Boost Clock",
    "Memory Clock", "Memory Size", "Memory Type", "Memory Bus", "Bandwidth",
    "TDP", "L1 Cache", "L2 Cache",
    "Shading Units", "FP32 (float)", "Tensor Cores", 'Matrix Cores']
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    raw_fixed = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace('\n', ' '), raw)
    raw_fixed = raw_fixed.replace('"', '')
    raw_fixed = re.sub(r'[ \t]+', ' ', raw_fixed)
    df = pd.read_csv(StringIO(raw_fixed), sep='|')
    df = df[relevant_columns]
    df['Product Name'] = df['Product Name'].apply(clean_gpu_name)
    df['Release Date'] = df['Release Date'].apply(format_date)
    df['Base Clock'] = df['Base Clock'].apply(extract_number)
    df['Boost Clock'] = df['Boost Clock'].apply(extract_number)
    df['Memory Clock'] = df['Memory Clock'].apply(extract_number)
    df['Memory Size'] = df['Memory Size'].apply(helpers.gb_to_mb)
    df['Memory Bus'] = df['Memory Bus'].apply(extract_int)
    df['Memory Type'] = df['Memory Type'].str.strip()
    df['Bandwidth'] = df['Bandwidth'].apply(helpers.tb_to_gb)
    df['TDP'] = df['TDP'].apply(extract_number)
    df['L1 Cache'] = df['L1 Cache'].apply(helpers.mb_to_kb)
    df['L2 Cache'] = df['L2 Cache'].apply(helpers.mb_to_kb)
    df['Shading Units'] = df['Shading Units'].apply(extract_int)
    df['FP32 (float)'] = df['FP32 (float)'].apply(helpers.tf_to_gf)
    df['Tensor Cores'] = df['Tensor Cores'].apply(extract_int)
    df['Matrix Cores'] = df['Matrix Cores'].apply(extract_int)
    df['Memory Size'] = df['Memory Size'].apply(helpers.gb_to_mb)

    """     # Percentage of missing values per column
    missing_percentage = df.isna().mean() * 100
    missing_counts = df.isna().sum()
    missing_stats = pd.DataFrame({
        'missing_count': missing_counts,
        'missing_percent': missing_percentage
    }).sort_values(by='missing_count', ascending=False)
    print(missing_stats) """
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
    name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    name = re.sub(r"\b(LHR|FULL\s*UNLOCK|ENGINEERING SAMPLE)\b", "", name, flags=re.IGNORECASE)
    name = name.strip()
    return name
