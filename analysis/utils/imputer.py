from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
import joblib
import pandas as pd

def impute_speedup(df: pd.DataFrame):
    relevant_columns = [
    "Product Name", "Architecture", "Release Date",
    "Base Clock", "Boost Clock",
    "Memory Clock", "Memory Size", "Memory Type", "Memory Bus", "Bandwidth",
    "TDP", "L1 Cache", "L2 Cache",
    "Shading Units", "CUDA", "FP32 (float)", "Tensor Cores", "BF16", "TF32"]

    sub = df.dropna(subset=["Speedup"])
    if sub.empty:
        return df

    X = sub[relevant_columns].fillna(0)
    y = sub["Speedup"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)

    tree = DecisionTreeRegressor(max_depth=6, random_state=42)
    forest = RandomForestRegressor(n_estimators=200, random_state=42)

    tree.fit(X_train, y_train)
    forest.fit(X_train, y_train)

    preds_tree = tree.predict(X_val)
    preds_forest = forest.predict(X_val)

    rmse_tree = root_mean_squared_error(y_val, preds_tree, squared=False)
    rmse_forest = root_mean_squared_error(y_val, preds_forest, squared=False)

    print(f"DecisionTree RMSE={rmse_tree:.3f}, RandomForest RMSE={rmse_forest:.3f}")

    best_model = forest if rmse_forest < rmse_tree else tree
    joblib.dump(best_model, "models/imputer_best.joblib")

    missing = df[df["Speedup"].isna()]
    if not missing.empty:
        df.loc[missing.index, "Speedup"] = best_model.predict(missing[relevant_columns].fillna(0))

    return df


def get_ai_cores(row):

    model = str(row.get("Model", "")).lower()

    if any(keyword in model for keyword in ["nvidia", "geforce", "gtx", "rtx"]):
        cores = row.get("Tensor Cores", 0)
        return 0 if pd.isna(cores) else cores
    
    elif any(keyword in model for keyword in ["amd", "radeon"]):
        cores = row.get("Matrix Cores", 0)
        return 0 if pd.isna(cores) else cores
    
    return None

def _set_tensor(row):
        nvidia_keywords = ["geforce", "gtx", "rtx", "nvidia"]
        amd_keywords = ['amd', 'radeon']
        if pd.isna(row["Tensor Cores"]):
            name_lower = str(row["Model"]).lower()
            if any(kw in name_lower for kw in nvidia_keywords):
                return 0    
        return row["Tensor Cores"]


def impute_gpu_for_mining_data(df: pd.DataFrame) -> pd.DataFrame:
    df["AI Cores"] = df.apply(get_ai_cores, axis=1)
    return df


def impute_speedup(df: pd.DataFrame):
    relevant_columns = [
    "Product Name", "Architecture", "Release Date",
    "Base Clock", "Boost Clock",
    "Memory Clock", "Memory Size", "Memory Type", "Memory Bus", "Bandwidth",
    "TDP", "L1 Cache", "L2 Cache",
    "Shading Units", "CUDA", "FP32 (float)", "Tensor Cores", "BF16", "TF32"]

    sub = df.dropna(subset=["Speedup"])
    if sub.empty:
        return df

    X = sub[relevant_columns].fillna(0)
    y = sub["Speedup"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)

    tree = DecisionTreeRegressor(max_depth=6, random_state=42)
    forest = RandomForestRegressor(n_estimators=200, random_state=42)

    tree.fit(X_train, y_train)
    forest.fit(X_train, y_train)

    preds_tree = tree.predict(X_val)
    preds_forest = forest.predict(X_val)

    rmse_tree = root_mean_squared_error(y_val, preds_tree, squared=False)
    rmse_forest = root_mean_squared_error(y_val, preds_forest, squared=False)

    print(f"DecisionTree RMSE={rmse_tree:.3f}, RandomForest RMSE={rmse_forest:.3f}")

    best_model = forest if rmse_forest < rmse_tree else tree
    joblib.dump(best_model, "models/imputer_best.joblib")

    missing = df[df["Speedup"].isna()]
    if not missing.empty:
        df.loc[missing.index, "Speedup"] = best_model.predict(missing[relevant_columns].fillna(0))

    return df
