import streamlit as st
import pandas as pd

# -----------------------------
# Streamlit Config & Intro
# -----------------------------
st.set_page_config(page_title="Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool (Custom Products Enabled)")

st.markdown("Add your own products below and compare to your competitors.")

# -----------------------------
# Global Pricing Logic Controls
# -----------------------------
col1, col2 = st.columns(2)
undercut_amount = col1.number_input("💸 Undercut Amount ($)", min_value=0.0, value=1.00, step=0.10)
floor_percent = col2.slider("🛡️ Price Floor (% of your price)", min_value=50, max_value=100, value=90)

st.divider()

# -----------------------------
# How Many Products to Add?
# -----------------------------
num_products = st.number_input("🛒 How many products would you like to enter?", min_value=1, max_value=20, value=5)

# -----------------------------
# Product Input Loop
# -----------------------------
updated_rows = []

for i in range(int(num_products)):
    st.subheader(f"🆕 Product #{i+1}")
    cols = st.columns(5)

    product_name = cols[0].text_input("Product Name", key=f"name_{i}")
    your_price = cols[1].number_input("Your Price", min_value=0.0, value=0.0, step=0.01, key=f"yp_{i}")
    comp_a = cols[2].number_input("Competitor A", min_value=0.0, value=0.0, step=0.01, key=f"a_{i}")
    comp_b = cols[3].number_input("Competitor B", min_value=0.0, value=0.0, step=0.01, key=f"b_{i}")
    comp_c = cols[4].number_input("Competitor C", min_value=0.0, value=0.0, step=0.01, key=f"c_{i}")

    lowest = min(comp_a, comp_b, comp_c) if any([comp_a, comp_b, comp_c]) else 0.0
    floor = round(your_price * (floor_percent / 100), 2)
    suggested = max(round(lowest - undercut_amount, 2), floor) if lowest > 0 else 0.0

    hit_floor = suggested == floor and suggested > 0
    icon = "🔒" if hit_floor else "💡"
    color = "red" if hit_floor else "lime"

    st.markdown(f"""
    <div style='line-height:1.3'>
        <span style='font-size: 18px;'>{icon} <strong>Suggested:</strong> 
        <span style='color:{color};'>${suggested:.2f}</span></span><br>
        <small><em>Floor: ${floor:.2f}, Undercut: ${undercut_amount:.2f}</em></small>
    </div>
    """, unsafe_allow_html=True)

    updated_rows.append({
        "Product": product_name or f"Product {i+1}",
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
# Final Table Output
# -----------------------------
result_df = pd.DataFrame(updated_rows)
st.markdown("## 📋 Final Suggested Prices")
st.dataframe(result_df, use_container_width=True)

csv = result_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name="repricing_suggestions.csv", mime='text/csv')
