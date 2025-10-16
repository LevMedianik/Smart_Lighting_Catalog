import joblib
import pandas as pd
from catboost import CatBoostRegressor

from app.config import MODEL_PATH, PREPROCESSOR_PATH

def load_model_and_preprocessor():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor
