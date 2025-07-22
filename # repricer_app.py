import streamlit as st
import pandas as pd

# -----------------------------
# Sample Product Data
# -----------------------------
products = [
    {"Product": "🖱️ Wireless Mouse", "Your Price": 24.99, "Competitor A": 30.00, "Competitor B": 40.00, "Competitor C": 40.00},
    {"Product": "🔊 Bluetooth Speaker", "Your Price": 49.99, "Competitor A": 54.99, "Competitor B": 51.00, "Competitor C": 52.49},
    {"Product": "🧲 USB-C Hub", "Your Price": 34.99, "Competitor A": 32.00, "Competitor B": 32.00, "Competitor C": 32.00},
    {"Product": "💻 Laptop Stand", "Your Price": 29.99, "Competitor A": 33.00, "Competitor B": 31.49, "Competitor C": 34.89},
    {"Product": "🎧 Noise Cancelling Headphones", "Your Price": 119.99, "Competitor A": 124.99, "Competitor B": 122.00, "Competitor C": 129.99}
]

# -----------------------------
# Streamlit App Config
# -----------------------------
st.set_page_config(page_title="Smart Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool (with Custom Rules)")

st.markdown("Fine-tune your pricing logic below:")

# -----------------------------
# Global Adjustable Settings
# -----------------------------
col1, col2 = st.columns(2)
undercut_amount = col1.number_input("💸 Undercut Amount ($)", min_value=0.0, value=1.00, step=0.10)
floor_percent = col2.slider("🛡️ Price Floor (% of your price)", min_value=50, max_value=100, value=90)

st.divider()

# -----------------------------
# Interactive Product Table
# -----------------------------
updated_rows = []

for idx, row in enumerate(products):
    st.subheader(f"{row['Product']}")
    cols = st.columns(5)

    your_price = cols[0].number_input("Your Price", value=row["Your Price"], key=f"yp_{idx}")
    comp_a = cols[1].number_input("Competitor A", value=row["Competitor A"], key=f"a_{idx}")
    comp_b = cols[2].number_input("Competitor B", value=row["Competitor B"], key=f"b_{idx}")
    comp_c = cols[3].number_input("Competitor C", value=row["Competitor C"], key=f"c_{idx}")

    lowest = min(comp_a, comp_b, comp_c)
    floor = round(your_price * (floor_percent / 100), 2)
    suggested = max(round(lowest - undercut_amount, 2), floor)

    hit_floor = suggested == floor

    icon = "🔒" if hit_floor else "💡"
    color = "red" if hit_floor else "lime"

    cols[4].markdown(f"""
    <div style='line-height:1.3'>
        <span style='font-size: 18px;'>{icon} <strong>Suggested:</strong> 
        <span style='color:{color};'>${suggested:.2f}</span></span><br>
        <small><em>Floor: ${floor:.2f}, Undercut: ${undercut_amount:.2f}</em></small>
    </div>
    """, unsafe_allow_html=True)

    updated_rows.append({
        "Product": row["Product"].replace("🖱️ ", "").replace("🔊 ", "").replace("🧲 ", "").replace("💻 ", "").replace("🎧 ", ""),
        "Your Price": your_price,
        "Competitor A": comp_a,
        "Competitor B": comp_b,
        "Competitor C": comp_c,
        "Lowest Competitor": lowest,
        "Suggested Price": suggested,
        "Price Floor (%)": f"{floor_percent}%",
        "Price Floor Value": floor,
        "Hit Floor": hit_floor
    })

# -----------------------------
# Final Table Display + Download
# -----------------------------
result_df = pd.DataFrame(updated_rows)
st.markdown("## 📋 Final Suggested Prices")
st.dataframe(result_df, use_container_width=True)

csv = result_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name="repricing_suggestions.csv", mime='text/csv')
