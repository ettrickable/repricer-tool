import streamlit as st
import pandas as pd
import io

# -----------------------------
# Streamlit Config & Intro
# -----------------------------
st.set_page_config(page_title="Smart Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool (Custom Products + Excel Export)")

st.markdown("Add your products below, set pricing rules, and track competitor pricing easily.")

# -----------------------------
# Global Settings
# -----------------------------
col1, col2 = st.columns(2)
undercut_amount = col1.number_input("💸 Undercut Amount ($)", min_value=0.0, value=1.00, step=0.10)
floor_percent = col2.slider("🛡️ Price Floor (% of your price)", min_value=50, max_value=100, value=90)

st.divider()

# -----------------------------
# Number of Products
# -----------------------------
num_products = st.number_input("🛒 How many products would you like to enter?", min_value=1, max_value=20, value=5)

# Emoji options for picker
emoji_options = {
    "🛒 Default": "",
    "🖱️ Mouse": "🖱️",
    "🎧 Headphones": "🎧",
    "💻 Laptop": "💻",
    "🔊 Speaker": "🔊",
    "📱 Phone": "📱",
    "⌚ Watch": "⌚",
    "🧲 USB Hub": "🧲",
    "📷 Camera": "📷",
    "🎮 Gaming": "🎮",
    "🧼 Cleaning": "🧼"
}

# -----------------------------
# Product Input Loop
# -----------------------------
updated_rows = []
export_rows = []

for i in range(int(num_products)):
    st.markdown("----")
    cols_top = st.columns([2, 2, 1])
    product_name_input = cols_top[0].text_input("Product Name", key=f"name_{i}")
    emoji_choice = cols_top[1].selectbox("Choose Icon", list(emoji_options.keys()), key=f"emoji_{i}")
    emoji = emoji_options[emoji_choice]

    display_name = f"{emoji} {product_name_input.strip()}" if product_name_input.strip() else f"🆕 Product #{i+1}"
    st.subheader(display_name)

    cols = st.columns(5)
    your_price = cols[0].number_input("Your Price", min_value=0.0, value=0.0, step=0.01, key=f"yp_{i}")
    comp_a = cols[1].number_input("Competitor A", min_value=0.0, value=0.0, step=0.01, key=f"a_{i}")
    comp_b = cols[2].number_input("Competitor B", min_value=0.0, value=0.0, step=0.01, key=f"b_{i}")
    comp_c = cols[3].number_input("Competitor C", min_value=0.0, value=0.0, step=0.01, key=f"c_{i}")

    lowest = min(comp_a, comp_b, comp_c) if any([comp_a, comp_b, comp_c]) else 0.0
    floor = round(your_price * (floor_percent / 100), 2)
    suggested = max(round(lowest - undercut_amount, 2), floor) if lowest > 0 else 0.0

    hit_floor = suggested == floor and suggested > 0
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
        "Product": f"{emoji} {product_name_input.strip()}" if product_name_input.strip() else f"Product {i+1}",
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

    export_rows.append({
        "Product": product_name_input.strip() or f"Product {i+1}",
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
# Final Table Display
# -----------------------------
st.markdown("## 📋 Final Suggested Prices")
result_df = pd.DataFrame(updated_rows)
st.dataframe(result_df, use_container_width=True)

# -----------------------------
# Excel Export (.xlsx)
# -----------------------------
excel_df = pd.DataFrame(export_rows)
output = io.BytesIO()

with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    excel_df.to_excel(writer, index=False, sheet_name="Prices")
    workbook = writer.book
    worksheet = writer.sheets["Prices"]
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:H", 18)

data = output.getvalue()

st.download_button(
    label="📥 Download Excel (.xlsx)",
    data=data,
    file_name="repricing_suggestions.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
