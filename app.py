import streamlit as st
from pipeline import run_pipeline
# Streamlit is used here to quickly build an interactive web UI
# for the sales prediction pipeline without extra frontend coding.


st.set_page_config(page_title="Amazon Product Sales Prediction", layout="wide")

st.title("Amazon Product Sales Prediction System")
st.markdown("""
Calculates the **estimated sales volume** (based on review counts) using Amazon data for a specific product.""")

category = st.text_input("Category", placeholder="e.g., headphones") #just for example i started with headphones
brand = st.text_input("Brand", placeholder="e.g., JBL")
model = st.text_input("Model", placeholder="e.g., 560 bt")
top_n = st.slider("Number of products to display", 1, 50, 10)
save_intermediate = st.checkbox("Save intermediate files (for debugging)", value=False)
# You’ll need to add more input fields here if you add more scraping parameters in the scraping file

if st.button("Start Prediction"):
    if not category or not brand:
        st.warning("Category and brand fields are required.")
    else:
        with st.spinner("Running pipeline, please wait..."):
            try:
                df_result = run_pipeline(category, brand, model, top_n, save_intermediate=save_intermediate)
                if df_result is None or df_result.empty:
                    st.warning("No prediction results available.")
                else:
                    st.success("Prediction completed successfully.")
                    st.dataframe(df_result[["title", "price", "rating", "predicted_reviews", "predicted_sales"]].head(top_n))

                    csv = df_result.to_csv(index=False).encode("utf-8")# Prepare CSV download of full results
                    filename = f"predicted_ranked_products_{brand}_{model}.csv".replace(" ", "_")
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name=filename,
                        mime="text/csv")
                    # Example extension:
                    # - Export results to a database using SQLAlchemy or any database you want
                    # - Send data to a REST API endpoint for further processing
                    # - Integrate with business intelligence tools like CRM

            except Exception as e:
                st.error(f"An error occurred: {e}")

