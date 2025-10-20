from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np


def _get_ai_cores(row):

    model = str(row.get("Model", "")).lower()

    if any(keyword in model for keyword in ["nvidia", "geforce", "gtx", "rtx"]):
        cores = row.get("Tensor Cores", 0)
        return 0 if pd.isna(cores) else cores
    
    elif any(keyword in model for keyword in ["amd", "radeon"]):
        cores = row.get("Matrix Cores", 0)
        return 0 if pd.isna(cores) else cores
      
    return None


def impute_numeric_columns(df: pd.DataFrame, random_state=42):
    df = df.copy()

    categorical_cols = ["Memory Type"]
    original_cats = df[categorical_cols].copy()

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical_cols),
        index=df.index
    )
    df = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "Revenue 24h" in numeric_cols:
        numeric_cols.remove("Revenue 24h")

    models = {
        "DecisionTree": DecisionTreeRegressor(random_state=random_state),
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=random_state)
    }

    total_rmse = {name: 0 for name in models.keys()}
    column_scores = {}

    for col in numeric_cols:
        n_missing = df[col].isna().sum()
        if n_missing == 0:
            continue

        df_train = df[df[col].notna()]
        df_pred = df[df[col].isna()]

        features = [c for c in numeric_cols if c != col]

        X = df_train[features].fillna(df_train[features].median())
        y = df_train[col]
        X_pred = df_pred[features].fillna(df_train[features].median())

        X_tr, X_val, y_tr, y_val = train_test_split(
            X, y, test_size=0.2, random_state=random_state
        )

        scores = {}
        for name, model in models.items():
            model.fit(X_tr, y_tr)
            y_pred_val = model.predict(X_val)
            rmse = np.sqrt(root_mean_squared_error(y_val, y_pred_val))
            scores[name] = rmse
            total_rmse[name] += rmse

        column_scores[col] = scores

    best_model_name = min(total_rmse, key=total_rmse.get)
    best_model_class = models[best_model_name]

    print(f"Global best model: {best_model_name} by total RMSE")
    print(f"Total RMSEs: {total_rmse}")

    for col in numeric_cols:
        if df[col].isna().sum() == 0:
            continue

        df_train = df[df[col].notna()]
        df_pred = df[df[col].isna()]
        if df_pred.empty:
            continue

        features = [c for c in numeric_cols if c != col]
        X = df_train[features].fillna(df_train[features].median())
        y = df_train[col]
        X_pred = df_pred[features].fillna(df_train[features].median())

        best_model = best_model_class
        best_model.fit(X, y)
        df.loc[df[col].isna(), col] = best_model.predict(X_pred)

    for col in categorical_cols:
        df[col] = original_cats[col]

    encoded_cols = encoder.get_feature_names_out(categorical_cols)
    df.drop(columns=encoded_cols, inplace=True)

    return df


def impute_gpu_for_mining_data(df: pd.DataFrame) -> pd.DataFrame:
    df["AI Cores"] = df.apply(_get_ai_cores, axis=1)
    df = df.drop(columns=["Tensor Cores", "Matrix Cores"], errors="ignore")
    df = impute_numeric_columns(df)
    return df

