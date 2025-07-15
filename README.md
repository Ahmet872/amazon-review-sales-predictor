# End to End Scalable Amazon Product Sales Estimation Pipeline

![Amazon Banner](assets/amazon_banner.png)

An end-to-end pipeline that scrapes Amazon product data and estimates product sales volume using machine learning.

---
## Overview
This repository provides an end-to-end, scalable pipeline for estimating Amazon product sales volume using machine learning and publicly available data. In e-commerce analytics, access to actual sales figures is often limited, but review counts serve as a reliable proxy for understanding demand trends. The project combines automated product data scraping, feature engineering, and a regression-based prediction model to enable several key functionalities.
Users can dynamically search and extract Amazon product listings. Raw product metadata such as price, brand, and title are cleaned and structured for analysis. Informative features including text length and brand encoding are engineered. A LightGBM-based model predicts the volume of product reviews. Potential sales are approximated through a flexible multiplier logic applied to predicted review counts.
The system architecture is designed for extensibility, allowing easy integration of new features or data sources. It supports both command line interface and an interactive web application, ensuring accessibility for users with varying technical backgrounds.
This project provides a solid foundation for developing market research tools, pricing intelligence systems, and competitor analysis dashboards.
---
## Purpose & Motivation
- **Objective:** Provide a fast, scalable, and modular solution to estimate the sales potential of products listed on Amazon.
- **Primary Use Case:** Product research and market analysis for e-commerce sellers, analysts, and brand managers.
- **Challenge:** Amazon does not publicly expose sales figures. The system uses review counts as a proxy, multiplied by a predefined conversion factor.

---
## Project Structure
amazon-sales-predictor/
- scraper.py              # Fetches product data from Amazon
- data_cleaning.py        # Cleans and formats raw scraped data
- train.py                # Trains ML model and saves it
- predict.py              # Loads model & makes predictions
- pipeline.py             # End-to-end orchestration pipeline
- app.py                  # Streamlit UI
- assets
- requirements.txt
- models/                 # Saved ML model & encoder
- output/                 # CSV outputs (optional)
- .env                    # API key (not committed)

---
## How It Works
1.	Scrape Products: Pulls Amazon search results using SerpAPI.
2.	Clean & Filter: Extracts relevant fields (title, price, reviews, brand).
3.	Train Model: Log-transform + LightGBM regression on review counts.
4.	Predict: Estimate log-reviews and scale to sales via a fixed multiplier.
5.	Streamlit App: User enters product info and gets top products + CSV.
---
## Example Use Case

```bash
streamlit run app.py
```

Input: Category = headphones, Brand = JBL, Model = bt 560
Output: Top N JBL headphone models ranked by predicted review count and sales.

---
## Installation
git clone https://github.com/yourusername/amazon-sales-predictor.git
cd amazon-sales-predictor
pip install -r requirements.txt
Add your API key in a .env file: 

```ini
SERPAPI_KEY=your_api_key_here
```

---
## Limitations
-	SerpAPI’s free tier has rate limits
-	Sales estimates rely on the assumption: Sales ≈ Reviews × 20
-	Actual sales may vary due to conversion rates, fake reviews, etc.

---
## Planned Improvements
While the system is fully functional and scalable by design, there are several areas identified for future improvement:
-	Model Precision: Currently, predictions rely on basic features like price, brand, and title length. Introducing advanced text embeddings, time based signals, and contextual user data can significantly improve accuracy
-	Static Sales Estimation Logic: The use of a fixed multiplier (reviews × 20) to estimate sales is a simplification. Category specific or dynamic multipliers based on historical data would yield more reliable estimates
-	Review Quality Signals: Fake or incentivized reviews are not filtered. Future versions will integrate heuristics or anomaly detection to downweight such distortions
-	Scaling & Scraper Reliability: The system depends on SerpAPI, which may introduce rate limits or inconsistencies. Alternative scraping backends or data pipelines will be evaluated for high-volume deployments
-	Category Sensitivity: The model currently treats all categories the same. Segmenting by product type can help account for differences in review behavior and conversion rates

---
## Technologies Used
-	Python: Core programming language used to build the entire pipeline, from data collection to prediction and UI.
-	Streamlit: Enables fast prototyping of interactive data apps without frontend coding.
-	LightGBM: Efficient and scalable gradient boosting framework and suited for tabular data and prediction.
-	Scikit-learn: Used for model selection preprocessing and evaluation metrics.
-	Pandas / NumPy: Essential tools for manipulating and analyzing structured tabular datasets.
-	SerpAPI: External web scraping API to extract structured Amazon product data, avoiding HTML parsing complexity.
-	dotenv: Keeps environment variables secure and separate from the codebase.
-	Requests: Standard HTTP client to make API calls to external services.
-	GitHub: Version control, issue tracking, and project collaboration.
-	ChatGPT (OpenAI): Used as a programming assistant and architectural design advisor during development.
-	Stack Overflow: Key resource for debugging, community driven implementation examples, and clarifying specific cases.

---
## Web Resources Used
-	SerpAPI: For fetching structured product data from Amazon programmatically.
-   Streamlit: For deploying a web-based interactive ML interface.
-	LightGBM Documentation: For model tuning and configuration.
-   Python dotenv: For managing sensitive environment variables.
-   Stack Overflow: For technical troubleshooting and code pattern references.
-   ChatGPT: Used during design and implementation phases to clarify logic, debug code, and ideate improvements.

---
## License
MIT License

---
## Contributing
Pull requests welcome. For major changes, open an issue first.

---
## Contact
Built by Seyyit Ahmet Arslan.
email: seyyitahmetarslan872@gmail.com
linkedin: www.linkedin.com/in/seyyit-ahmet-arslan-5b1666233
