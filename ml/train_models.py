# ==============================================================
# ЭТАП 3. ОБУЧЕНИЕ И СРАВНЕНИЕ МОДЕЛЕЙ (MLflow)
# ==============================================================
import numpy as np
import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

# ==============================================================
# 1) Загрузка данных
# ==============================================================
data = np.load("data/train_test_ready.npz")
X_train, X_test = data["X_train"], data["X_test"]
y_train, y_test = data["y_train"], data["y_test"]

# ==============================================================
# 2) Настройка MLflow
# ==============================================================
mlflow.set_tracking_uri("file:./ml/mlruns")
mlflow.set_experiment("lighting_recommender")

# ==============================================================
# 3) Набор моделей
# ==============================================================
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.001),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
    "KNN": KNeighborsRegressor(n_neighbors=5),
    "MLPRegressor": MLPRegressor(hidden_layer_sizes=(128, 64), max_iter=300, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, random_state=42),
    "LightGBM": LGBMRegressor(n_estimators=500, learning_rate=0.05, num_leaves=31, random_state=42),
    "CatBoost": CatBoostRegressor(verbose=0, iterations=500, learning_rate=0.05, depth=8, random_state=42)
    }

# ==============================================================
# 4) Цикл обучения и логирования
# ==============================================================
results = []

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = root_mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_param("model_name", name)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, artifact_path="model")

        results.append((name, rmse, mae, r2))
        print(f"{name}: RMSE={rmse:.3f}, MAE={mae:.3f}, R2={r2:.3f}")

# ==============================================================
# 5) Определение лучшей модели
# ==============================================================
best = sorted(results, key=lambda x: x[1])[0]  # по минимальному RMSE
print("\nЛучшая модель:")
print(f"{best[0]} — RMSE={best[1]:.3f}, R2={best[3]:.3f}")

# Сохранение финального артефакта
best_model = models[best[0]]
joblib.dump(best_model, f"ml/best_model.pkl")
print(f"Лучшая модель сохранена: ml/best_model.pkl")
