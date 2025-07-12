# Runs the full pipeline: scraping, cleaning, training, prediction and optional saving.
import pandas as pd
import logging
import os
from scraper import SerpAPIAmazonScraper
from data_cleaning import clean_amazon_products
from typing import Optional
from predict import predict



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
# Configure logging to display timestamps, log level, and messages

def run_pipeline(
    category: str, brand: str, model: str,
    top_n: int = 20, save_intermediate: bool = False) -> Optional[pd.DataFrame]:
    # Validate inputs and run the full product prediction pipeline.

    if not all([category.strip(), brand.strip(), model.strip()]):
        raise ValueError("Category, brand, and model cannot be empty.")

    query = f"{brand} {model} {category}".strip()# Build search query from user inputs and log it
    logging.info(f" Searching products with query: {query}")

    try:
        scraper = SerpAPIAmazonScraper()
        raw_products = scraper.search_products(query)
    except Exception as e:
        logging.error(f"Scraping error: {e}")
        return None

    if not raw_products:
        logging.warning("No products found. Aborting pipeline.")
        return None

    try:
        cleaned_df = clean_amazon_products(raw_products)
    except Exception as e:
        logging.error(f"Data cleaning error: {e}")
        return None

    if cleaned_df.empty:
        logging.warning("Cleaned data is empty. Aborting pipeline.")
        return None
    if save_intermediate:
        os.makedirs("output", exist_ok=True)
        cleaned_path = f"output/cleaned_products_{brand}_{model}.csv"
        cleaned_df.to_csv(cleaned_path, index=False)
        logging.info(f"Cleaned data saved as '{cleaned_path}'.")
    else:
        cleaned_path = None

    try:
        result_df = predict(
            model_path="models/model.pkl",
            encoder_path="models/brand_encoder.pkl",
            input_df=cleaned_df,
            output_csv=None,
            top_n=top_n,
            verbose=True)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return None

    if save_intermediate:
        os.makedirs("output", exist_ok=True)
        output_path = f"output/predicted_ranked_products_{brand}_{model}.csv"
        result_df.to_csv(output_path, index=False)
        logging.info(f"Prediction results saved as '{output_path}'.")
    # Save prediction results to CSV if requested
    
    return result_df

