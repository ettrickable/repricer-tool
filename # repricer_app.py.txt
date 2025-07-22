# repricer_app.py

import streamlit as st
import pandas as pd

# -----------------------------
# 💡 Sample Product Data (You can change these!)
# -----------------------------
products = [
    {
        "Product": "Wireless Mouse",
        "Your Price": 24.99,
        "Competitor A": 26.99,
        "Competitor B": 25.49,
        "Competitor C": 27.89
    },
    {
        "Product": "Bluetooth Speaker",
        "Your Price": 49.99,
        "Competitor A": 54.99,
        "Competitor B": 51.00,
        "Competitor C": 52.49
    },
    {
        "Product": "USB-C Hub",
        "Your Price": 34.99,
        "Competitor A": 39.99,
        "Competitor B": 37.50,
        "Competitor C": 36.89
    },
    {
        "Product": "Laptop Stand",
        "Your Price": 29.99,
        "Competitor A": 33.00,
        "Competitor B": 31.49,
        "Competitor C": 34.89
    },
    {
        "Product": "Noise Cancelling Headphones",
        "Your Price": 119.99,
        "Competitor A": 124.99,
        "Competitor B": 122.00,
        "Competitor C": 129.99
    }
]

# -----------------------------
# 🚀 Streamlit App Starts Here
# -----------------------------
st.set_page_config(page_title="Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool")

st.markdown("""
Adjust your prices and your competitors'.  
This tool will suggest a new price that’s **$1 below the lowest competitor**,  
but **never lower than 90%** of your original price.
""")

updated_rows = []

# -----------------------------
# 🔄 Interactive Inputs
# -----------------------------
for idx, row in enumerate(products):
    st.subheader(f"🛍️ {row['Product']}")
    cols = st.columns(5)
    your_price = cols[0].number_input("Your Price", value=row["Your Price"], key=f"yp_{idx}")
    comp
