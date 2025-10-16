import os
from dotenv import load_dotenv
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "ml/best_model.pkl")
PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH", "ml/preprocessor.pkl")
FIXTURES_PATH = os.getenv("FIXTURES_PATH", "data/fixtures.csv")
TOP_N = int(os.getenv("TOP_N", 3))
