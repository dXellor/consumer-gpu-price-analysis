import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import math

def predict_revenue(df: pd.DataFrame, important_features: list, revenue_col="Revenue 24h"):
    available_features = [f for f in important_features if f in df.columns]

    df_model = df[available_features + [revenue_col]].copy()

    categorical_features = df_model.select_dtypes(include=['object']).columns.tolist()
    if categorical_features:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded = encoder.fit_transform(df_model[categorical_features])
        encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_features), index=df_model.index)
        df_model = pd.concat([df_model.drop(columns=categorical_features), encoded_df], axis=1)


    df_known = df_model[df_model[revenue_col].notnull()].copy()
    df_missing = df_model[df_model[revenue_col].isnull()].copy()


    X = df_known.drop(columns=[revenue_col])
    y = df_known[revenue_col]

    # 4️⃣ Train/Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\n📊 Podela skupa: train={len(X_train)}, test={len(X_test)}")

    # 5️⃣ Definicija modela
    models = {
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(random_state=42, n_estimators=200)
    }

    metrics = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = math.sqrt(mean_squared_error(y_test, preds))
        metrics[name] = {"MAE": mae, "RMSE": rmse}
        print(f"\n📈 {name}:")
        print(f"   MAE  = {mae:.4f}")
        print(f"   RMSE = {rmse:.4f}")

    # 6️⃣ Odabir najboljeg modela po MAE
    best_model_name = min(metrics, key=lambda k: metrics[k]["MAE"])
    best_model = models[best_model_name]
    print(f"\n🏆 Najbolji model po MAE: {best_model_name}")

    best_model_name = min(metrics, key=lambda k: metrics[k]["RMSE"])
    best_model = models[best_model_name]
    print(f"\n🏆 Najbolji model po RMSE: {best_model_name}")


    # 7️⃣ Predikcija za redove bez Revenue vrednosti
    if not df_missing.empty:
        X_missing = df_missing.drop(columns=[revenue_col])
        predicted_values = best_model.predict(X_missing)
        df.loc[df[revenue_col].isnull(), revenue_col] = predicted_values
        print(f"\n🔮 Popunjeno {len(predicted_values)} nedostajućih vrednosti kolone '{revenue_col}'.")

    return df, metrics, best_model_name
