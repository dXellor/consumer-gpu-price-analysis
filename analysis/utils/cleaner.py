import re
import pandas as pd
from io import StringIO
import utils.helpers as helpers


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

    df['Model'] = df['Model'].apply(helpers.clean_gpu_name)
    df = df.drop_duplicates(subset=["Model"], keep="first")
    
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
    df['Hashrate'] = df['Hashrate'].apply(helpers.to_num)

    df['Revenue 24h'] = df['Revenue 24h'].apply(helpers.clean_currency)

    return df[['Model', 'Release Date', 'Hashrate', 'Revenue 24h']]

        
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
    df['Product Name'] = df['Product Name'].apply(helpers.clean_gpu_name)
    df['Release Date'] = df['Release Date'].apply(helpers.format_date)
    df['Base Clock'] = df['Base Clock'].apply(helpers.extract_number)
    df['Boost Clock'] = df['Boost Clock'].apply(helpers.extract_number)
    df['Memory Clock'] = df['Memory Clock'].apply(helpers.extract_number)
    df['Memory Size'] = df['Memory Size'].apply(helpers.gb_to_mb)
    df['Memory Bus'] = df['Memory Bus'].apply(helpers.extract_int)
    df['Memory Type'] = df['Memory Type'].str.strip()
    df['Bandwidth'] = df['Bandwidth'].apply(helpers.tb_to_gb)

    df['TDP'] = df['TDP'].apply(helpers.extract_number)
    df['L1 Cache'] = df['L1 Cache'].apply(helpers.mb_to_kb)
    df['L2 Cache'] = df['L2 Cache'].apply(helpers.mb_to_kb)
    df['Shading Units'] = df['Shading Units'].apply(helpers.extract_int)
    df['FP32 (float)'] = df['FP32 (float)'].apply(helpers.tf_to_gf)
    df['Tensor Cores'] = df['Tensor Cores'].apply(helpers.extract_int)
    df['Matrix Cores'] = df['Matrix Cores'].apply(helpers.extract_int)

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
    df['GPU Name'] = df['GPU Name'].apply(helpers.clean_gpu_name)
    df['Speedup'] = df['Speedup'].apply(helpers.to_num)
    return df


