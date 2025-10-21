import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, f_oneway

def analyze_revenue_influence(df: pd.DataFrame, revenue_col="Revenue 24h"):
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != revenue_col]
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols = [c for c in categorical_cols if c != revenue_col]
    categorical_cols.remove('Model')
    results = []

    for col in numeric_cols:
        if df[col].nunique() > 1: 
            pearson_corr, pearson_p = pearsonr(df[col], df[revenue_col])
            spearman_corr, spearman_p = spearmanr(df[col], df[revenue_col])
            results.append({
                'attribute': col,
                'type': 'numeric',
                'pearson_corr': pearson_corr,
                'pearson_p': pearson_p,
                'spearman_corr': spearman_corr,
                'spearman_p': spearman_p
            })

    for col in categorical_cols:
        groups = [group[revenue_col].values for name, group in df.groupby(col) if len(group) > 0]
        if len(groups) > 1:
            f_stat, p_value = f_oneway(*groups)
            results.append({
                'attribute': col,
                'type': 'categorical',
                'f_stat': f_stat,
                'p_value': p_value
            })

    numeric_results = sorted([r for r in results if r['type']=='numeric'], 
                             key=lambda x: abs(x['pearson_corr']), reverse=True)

    categorical_results = sorted([r for r in results if r['type']=='categorical'], 
                                 key=lambda x: x['p_value'])

    return numeric_results, categorical_results
