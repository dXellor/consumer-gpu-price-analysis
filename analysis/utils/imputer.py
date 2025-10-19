from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
import joblib
import pandas as pd


def _get_ai_cores(row):

    model = str(row.get("Model", "")).lower()

    if any(keyword in model for keyword in ["nvidia", "geforce", "gtx", "rtx"]):
        cores = row.get("Tensor Cores", 0)
        return 0 if pd.isna(cores) else cores
    
    elif any(keyword in model for keyword in ["amd", "radeon"]):
        cores = row.get("Matrix Cores", 0)
        return 0 if pd.isna(cores) else cores
    
    return None


def impute_gpu_for_mining_data(df: pd.DataFrame) -> pd.DataFrame:
    df["AI Cores"] = df.apply(_get_ai_cores, axis=1)
    return df

