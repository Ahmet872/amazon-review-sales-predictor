import pandas as pd
import numpy as np
import os
import logging
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
from typing import Tuple
# Train a LightGBM regression model to estimate product review counts (as a proxy for sales).
# LightGBM is selected for its speed, accuracy, and robustness with structured/tabular data.
# Outputs the best model and label encoder for later prediction use.



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_data(file_path: str) -> pd.DataFrame:# Ensure the file exists before loading
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["price", "rating", "reviews", "title", "brand", "model"])
    df["log_reviews"] = np.log1p(df["reviews"])# Create engineered features to enhance model input
    df["title_length"] = df["title"].apply(len)
    df["model_length"] = df["model"].apply(len)
    return df

def encode_brands(df: pd.DataFrame) -> Tuple[pd.DataFrame, LabelEncoder]:
    brands = df["brand"].astype(str).unique().tolist()
    if "unknown" not in brands:# Ensure "unknown" is included for unseen brands at inference time
        brands.append("unknown")
    le_brand = LabelEncoder()
    le_brand.fit(brands)
    df["brand_encoded"] = df["brand"].astype(str).apply(lambda x: x if x in brands else "unknown")
    df["brand_encoded"] = le_brand.transform(df["brand_encoded"])
    return df, le_brand

def train_and_evaluate(df: pd.DataFrame, le_brand: LabelEncoder):
    FEATURES = ["price", "rating", "title_length", "model_length", "brand_encoded"]
    X = df[FEATURES]
    y = df["log_reviews"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)# Train/test split

    model = LGBMRegressor(random_state=42) 
    param_grid = {
        "num_leaves": [31, 50, 70],
        "learning_rate": [0.01, 0.05, 0.1],
        "n_estimators": [100, 200, 300]}

    grid_search = GridSearchCV(model, param_grid, cv=5, scoring="neg_root_mean_squared_error", verbose=1)
    # Grid search with 5-fold CV to find best hyperparameters
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    # Evaluate on test set using multiple metrics
    
    logging.info(f"Best Params: {grid_search.best_params_}")
    logging.info(f"Test RMSE: {rmse:.4f}")
    logging.info(f"Test R2: {r2:.4f}")
    logging.info(f"Test MAE: {mae:.4f}")

    os.makedirs("models", exist_ok=True)
    with open("models/model_lgbm.pkl", "wb") as f:
        pickle.dump(best_model, f)
    with open("models/brand_encoder.pkl", "wb") as f:
        pickle.dump(le_brand, f)
    logging.info("Model and encoder saved successfully.")
    # Save model and encoder for later use

def train_model(file_path: str = "cleaned_products.csv"):
    # Wrapper to handle the training pipeline end-to-end with error logging
    try:
        df = load_data(file_path)
        df = preprocess_data(df)
        df, le_brand = encode_brands(df)
        train_and_evaluate(df, le_brand)
    except Exception as e:
        logging.error(f"Training failed: {e}")

if __name__ == "__main__":
    train_model()
