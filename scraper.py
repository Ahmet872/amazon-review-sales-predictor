# Uses SerpAPI to scrape Amazon product data based on a search query.
import os
import re
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import logging


# Load environment variables from .env file (make sure your SERPAPI_KEY is in there!)
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SerpAPIAmazonScraper: #can be used another api, but today as a easy and free to use apı i decided to this

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY") # need to have an api key
        if not self.api_key:
            raise ValueError("SERPAPI_KEY is missing. Define it in a .env file.")
        self.base_url = "https://serpapi.com/search"


    def search_products(self, query: str, amazon_domain: str = "amazon.com") -> List[Dict[str, Any]]:

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        params = {
            "engine": "amazon",
            "amazon_domain": amazon_domain,
            "api_key": self.api_key,
            "k": query}

        try:
            logging.info(f"Sending request to SerpAPI for query: {query}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("organic_results", [])
            logging.info(f"{len(results)} results retrieved for query: {query}")
            return results
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except ValueError:
            raise RuntimeError("Invalid JSON received from SerpAPI.")
            

def format_product(product: Dict[str, Any]) -> Dict[str, str]: # Extract and clean up product details
    title = product.get("title", "N/A")
    price = product.get("price", {})
    price = price.get("raw", "N/A") if isinstance(price, dict) else str(price)
    rating = product.get("rating", "N/A")
    reviews_raw = product.get("reviews", "N/A") #It's impossible to have the exact sale quantity with free api so we will go for reviews
    # as a scalable model you can scrape several more things just buy adding here
    
    if isinstance(reviews_raw, dict):
        reviews = reviews_raw.get("count", "N/A")
    elif isinstance(reviews_raw, str):
        reviews = re.sub(r"[^\d]", "", reviews_raw) or "N/A"
    else:
        reviews = str(reviews_raw) or "N/A"
    return {
        "title": title,
        "price": price,
        "rating": str(rating),
        "reviews": reviews}


def run_cli():
    print("let scraping begin")
    category = input("Enter product category: ")
    brand = input("Enter brand: ")
    model = input("Enter model: ")
    query = f"{brand} {model} {category}".strip() # Build a simple query string
    scraper = SerpAPIAmazonScraper()

    try:
        results = scraper.search_products(query)
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    if not results:
        print("No results found.")
        return
    print(f"\nSearch Results for '{query}':\n")

    for i, product in enumerate(results, 1):
        formatted = format_product(product)
        print(f"{i}. {formatted['title']}\n Price: {formatted['price']} , Rating: {formatted['rating']} , Reviews: {formatted['reviews']}\n")

if __name__ == "__main__":
    run_cli()
