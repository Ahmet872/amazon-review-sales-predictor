# Cleans and parses raw Amazon product data into structured format for modeling.
import pandas as pd
import re
from typing import List, Dict, Tuple, Optional, Union



def extract_brand_model(title: str) -> Tuple[str, str]:

    common_words = {"the", "a", "an", "for", "with", "by", "and", "of"}
    # Common English stopwords, sourced from typical NLP lists; can be extended as needed 
    words = [word for word in title.split() if word.lower() not in common_words]
    brand = words[0] if words else "Unknown"

    for word in words[1:]:
        if re.match(r"^[A-Za-z0-9\-]+$", word):
            return brand, word
    return brand, "Unknown"


def parse_price(price_raw: Union[str, Dict[str, str]]) -> Optional[float]:

    if isinstance(price_raw, dict):
        price_str = price_raw.get("raw", "")
    else:
        price_str = str(price_raw)
    price_str = re.sub(r"[^\d\.]", "", price_str)

    try:
        return float(price_str)
    except (ValueError, AttributeError):
        return None
#Parses and converts raw price data (str or dict) into a float value.


def parse_rating(rating_raw: Union[str, float, int]) -> float:

    try:
        return float(rating_raw)
    except (ValueError, TypeError):
        return 0.0


def parse_reviews(reviews_raw: Union[str, Dict[str, str], int]) -> int:
    # Convert raw price (string or dict) to float after cleaning non-numeric chars  
    if isinstance(reviews_raw, dict):
        reviews_str = reviews_raw.get("count", "0")
    else:
        reviews_str = str(reviews_raw)
    try:
        return int(re.sub(r"[^\d]", "", reviews_str))
    except (ValueError, AttributeError):
        return 0


def clean_amazon_products(raw_products: List[Dict], model_filter: str = "") -> pd.DataFrame:

    cleaned_data = []
    total = len(raw_products)

    for product in raw_products:
        title = product.get("title")
        if not title:
            continue
        if model_filter and model_filter.lower() not in title.lower():# Filter by model substring if model_filter provided
            continue

        # Parse raw fields into usable numeric values
        price = parse_price(product.get("price", ""))
        rating = parse_rating(product.get("rating", 0))
        reviews = parse_reviews(product.get("reviews", "0"))
        brand, extracted_model = extract_brand_model(title)
        
        if price is not None: # Only include if price parsing succeeded
            cleaned_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "brand": brand,
                "model": extracted_model})

    if not cleaned_data:
        raise ValueError(f"No valid products found. Total scraped: {total}")
    return pd.DataFrame(cleaned_data)
    # Raise error if no valid products were found
