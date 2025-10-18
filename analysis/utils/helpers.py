import pandas as pd
import re


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
    return value


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
    return value


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