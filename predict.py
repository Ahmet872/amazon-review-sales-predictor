# Loads a trained model and predicts product review counts (as a proxy for sales) from given input data.
import pickle
import pandas as pd
import numpy as np
import os
from typing import Optional



def predict(
    model_path: str,
    encoder_path: str,
    input_csv: Optional[str] = None,
    output_csv: Optional[str] = None,
    top_n: int = 20,
    verbose: bool = True,
    input_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:


    if input_df is None:
        if input_csv is None:
            raise ValueError("Either input_csv or input_df must be provided.")
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"File not found: {input_csv}")
        df = pd.read_csv(input_csv)
    else:
        df = input_df.copy()

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(encoder_path):
        raise FileNotFoundError(f"Encoder file not found: {encoder_path}")
    

    with open(model_path, "rb") as f:
        model = pickle.load(f)  # Load trained model and label encoder
    with open(encoder_path, "rb") as f:
        brand_encoder = pickle.load(f)


    # Validate that input DataFrame includes all necessary columns
    required_cols = {"title", "price", "rating", "brand", "model"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in input data: {missing}")

    df["brand"] = df["brand"].fillna("unknown").astype(str)

    known_brands = set(brand_encoder.classes_)# Get the set of known brand labels from the encoder
    df["brand"] = df["brand"].apply(lambda x: x if x in known_brands else "unknown")
    df["title_length"] = df["title"].apply(lambda x: len(str(x)))# Feature engineering: title and model string lengths
    df["model_length"] = df["model"].apply(lambda x: len(str(x)))
    df["brand_encoded"] = brand_encoder.transform(df["brand"])

    features = ["price", "rating", "title_length", "model_length", "brand_encoded"]
    X = df[features]

    df["predicted_log_reviews"] = model.predict(X)
    df["predicted_reviews"] = np.expm1(df["predicted_log_reviews"]).round().astype(int)# Convert log(review) back to actual review counts
    df["predicted_sales"] = (df["predicted_reviews"] * 20).astype(int)
    # Estimate sales by multiplying predicted reviews by 20 (assumed conversion rate)
    df_sorted = df.sort_values(by="predicted_reviews", ascending=False)

    if verbose:# If verbose mode is enabled, print top-N predicted products
        print(f"Top {top_n} products by predicted reviews:\n")
        print(df_sorted[["title", "price", "rating", "predicted_reviews"]].head(top_n).to_string(index=False))

    if output_csv:
        df_sorted.to_csv(output_csv, index=False)
        if verbose:
            print(f"\n Predictions saved to '{output_csv}'")

    return df_sorted
