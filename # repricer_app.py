import streamlit as st
import pandas as pd
import io

# -----------------------------
# App Settings
# -----------------------------
st.set_page_config(page_title="Smart Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool (with Excel Export)")

st.markdown("Set pricing logic, enter your products, compare to competitors, and download clean Excel reports.")

# -----------------------------
# Global Price Rules
# -----------------------------
col1, col2 = st.columns(2)
undercut_amount = col1.number_input("💸 Undercut Amount ($)", min_value=0.0, value=1.00, step=0.10)
floor_percent = col2.slider("🛡️ Price Floor (% of your price)", min_value=50, max_value=100, value=90)

st.divider()

# -----------------------------
# Competitor Naming Section
# -----------------------------
st.markdown("### 🏷️ Competitor Names")
ccol1, ccol2, ccol3 = st.columns(3)
comp1_name = ccol1.text_input("Competitor 1 Label", value="Competitor A")
comp2_name = ccol2.text_input("Competitor 2 Label", value="Competitor B")
comp3_name = ccol3.text_input("Competitor 3 Label", value="Competitor C")

st.divider()

# -----------------------------
# Product Quantity
# -----------------------------
num_products = st.number_input("📦 Number of products to enter", min_value=1, max_value=20, value=5)

# Emoji dropdown
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
# Main Product Loop
# -----------------------------
export_data = []
ui_data = []

for i in range(int(num_products)):
    st.markdown("---")
    top_cols = st.columns([2, 2, 1])
    name = top_cols[0].text_input("Product Name", key=f"name_{i}")
    emoji_choice = top_cols[1].selectbox("Icon", list(emoji_options.keys()), key=f"emoji_{i}")
    emoji = emoji_options[emoji_choice]
    display_name = f"{emoji} {name.strip()}" if name.strip() else f"🆕 Product #{i+1}"

    st.subheader(display_name)

    cols = st.columns(5)
    your_price = cols[0].number_input("Your Price", 0.0, step=0.01, key=f"yp_{i}")
    comp_a = cols[1].number_input(f"{comp1_name}", 0.0, step=0.01, key=f"a_{i}")
    comp_b = cols[2].number_input(f"{comp2_name}", 0.0, step=0.01, key=f"b_{i}")
    comp_c = cols[3].number_input(f"{comp3_name}", 0.0, step=0.01, key=f"c_{i}")

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

    ui_data.append({
        "Product": display_name,
        "Your Price": your_price,
        comp1_name: comp_a,
        comp2_name: comp_b,
        comp3_name: comp_c,
        "Lowest Competitor": lowest,
        "Suggested Price": suggested,
        "Price Floor (%)": f"{floor_percent}%",
        "Price Floor Value": floor,
        "Hit Floor": hit_floor
    })

    export_data.append({
        "Product": name.strip() or f"Product {i+1}",
        "Your Price": your_price,
        comp1_name: comp_a,
        comp2_name: comp_b,
        comp3_name: comp_c,
        "Lowest Competitor": lowest,
        "Suggested Price": suggested,
        "Price Floor (%)": f"{floor_percent}%",
        "Price Floor Value": floor,
        "Hit Floor": hit_floor
    })

# -----------------------------
# Final Table View
# -----------------------------
st.markdown("## 📊 Final Suggested Prices")
df_ui = pd.DataFrame(ui_data)
st.dataframe(df_ui, use_container_width=True)

# -----------------------------
# Excel Download (.xlsx)
# -----------------------------
df_export = pd.DataFrame(export_data)
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df_export.to_excel(writer, index=False, sheet_name="Repricing")
    worksheet = writer.sheets["Repricing"]
    worksheet.set_column("A:A", 30)  # Product column
    worksheet.set_column("B:H", 18)  # Others
data = output.getvalue()

st.download_button(
    "📥 Download Excel (.xlsx)",
    data=data,
    file_name="repricing_suggestions.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
