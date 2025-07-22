import streamlit as st
import pandas as pd

products = [
    {"Product": "Wireless Mouse", "Your Price": 24.99, "Competitor A": 26.99, "Competitor B": 25.49, "Competitor C": 27.89},
    {"Product": "Bluetooth Speaker", "Your Price": 49.99, "Competitor A": 54.99, "Competitor B": 51.00, "Competitor C": 52.49},
    {"Product": "USB-C Hub", "Your Price": 34.99, "Competitor A": 39.99, "Competitor B": 37.50, "Competitor C": 36.89},
    {"Product": "Laptop Stand", "Your Price": 29.99, "Competitor A": 33.00, "Competitor B": 31.49, "Competitor C": 34.89},
    {"Product": "Noise Cancelling Headphones", "Your Price": 119.99, "Competitor A": 124.99, "Competitor B": 122.00, "Competitor C": 129.99}
]

st.set_page_config(page_title="Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool")

updated_rows = []

for idx, row in enumerate(products):
    st.subheader(f"🛍️ {row['Product']}")
    cols = st.columns(5)
    
    your_price = cols[0].number_input("Your Price", value=row["Your Price"], key=f"yp_{idx}")
    comp_a = cols[1].number_input("Competitor A", value=row["Competitor A"], key=f"a_{idx}")
    comp_b = cols[2].number_input("Competitor B", value=row["Competitor B"], key=f"b_{idx}")
    comp_c = cols[3].number_input("Competitor C", value=row["Competitor C"], key=f"c_{idx}")
    
    lowest = min(comp_a, comp_b, comp_c)
    floor = round(your_price * 0.9, 2)
    suggested = max(round(lowest - 1, 2), floor)

    cols[4].markdown(f"**💡 Suggested:**  \n💲**${suggested:.2f}** *(Floor: ${floor:.2f})*")

    updated_rows.append({
        "Product": row["Product"],
        "Your Price": your_price,
        "Competitor A": comp_a,
        "Competitor B": comp_b,
        "Competitor C": comp_c,
        "Lowest Competitor": lowest,
        "Suggested Price": suggested,
        "Price Floor (90%)": floor
    })

result_df = pd.DataFrame(updated_rows)
st.markdown("## 📋 Final Suggested Prices")
st.dataframe(result_df)

csv = result_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name="repricing_suggestions.csv", mime='text/csv')
