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
