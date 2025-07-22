import streamlit as st
import pandas as pd
import io
import json

# -----------------------------
# App Setup
# -----------------------------
st.set_page_config(page_title="Smart Repricing Tool", layout="wide")
st.title("💰 Smart Repricing Tool")

st.markdown("Set your pricing logic, enter product names, compare competitor prices, and export to Excel. You can now save and load your session!")

# -----------------------------
# Save/Load Section
# -----------------------------
st.sidebar.header("💾 Save / Load")
save_filename = st.sidebar.text_input("Filename to Save As", value="repricer_session.json")

if st.sidebar.button("💾 Save Progress"):
    session_data = {
        "undercut_amount": st.session_state.get("undercut_amount", 1.00),
        "floor_percent": st.session_state.get("floor_percent", 90),
        "num_competitors": st.session_state.get("num_competitors", 3),
        "competitor_names": st.session_state.get("competitor_names", []),
        "num_products": st.session_state.get("num_products", 5),
        "products": []
    }

    for i in range(session_data["num_products"]):
        product = {
            "name": st.session_state.get(f"prod_name_{i}", ""),
            "emoji": st.session_state.get(f"emoji_{i}", ""),
            "your_price": st.session_state.get(f"your_price_{i}", 0.0),
            "competitor_prices": [
                st.session_state.get(f"comp_{j}_{i}", 0.0) for j in range(session_data["num_competitors"])
            ]
        }
        session_data["products"].append(product)

    json_data = json.dumps(session_data)
    st.sidebar.download_button("⬇️ Download .json", json_data, file_name=save_filename, mime="application/json")

uploaded_file = st.sidebar.file_uploader("📂 Load Previous .json", type="json")

if uploaded_file:
    loaded_data = json.load(uploaded_file)
    st.session_state["undercut_amount"] = loaded_data["undercut_amount"]
    st.session_state["floor_percent"] = loaded_data["floor_percent"]
    st.session_state["num_competitors"] = loaded_data["num_competitors"]
    st.session_state["competitor_names"] = loaded_data["competitor_names"]
    st.session_state["num_products"] = loaded_data["num_products"]
    for i, product in enumerate(loaded_data["products"]):
        st.session_state[f"prod_name_{i}"] = product["name"]
        st.session_state[f"emoji_{i}"] = product["emoji"]
        st.session_state[f"your_price_{i}"] = product["your_price"]
        for j, val in enumerate(product["competitor_prices"]):
            st.session_state[f"comp_{j}_{i}"] = val

# -----------------------------
# Global Pricing Settings
# -----------------------------
col1, col2 = st.columns(2)
undercut_amount = col1.number_input("💸 Undercut Amount ($)", min_value=0.0, value=st.session_state.get("undercut_amount", 1.00), step=0.10, key="undercut_amount")
floor_percent = col2.slider("🛡️ Price Floor (% of your price)", min_value=50, max_value=100, value=st.session_state.get("floor_percent", 90), key="floor_percent")

st.divider()

# -----------------------------
# Competitor Count and Labels
# -----------------------------
num_competitors = st.slider("👥 Number of Competitors", 1, 5, value=st.session_state.get("num_competitors", 3), key="num_competitors")
comp_cols = st.columns(num_competitors)
default_names = [f"Competitor {chr(65+i)}" for i in range(num_competitors)]
competitor_names = [comp_cols[i].text_input(f"Competitor {i+1} Name", value=(st.session_state.get("competitor_names", default_names))[i], key=f"comp_name_{i}") for i in range(num_competitors)]
st.session_state["competitor_names"] = competitor_names

st.divider()

# -----------------------------
# Number of Products
# -----------------------------
num_products = st.number_input("📦 Number of Products", min_value=1, max_value=20, value=st.session_state.get("num_products", 5), key="num_products")

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
# Product Loop
# -----------------------------
ui_data = []
excel_data = []

for i in range(num_products):
    st.markdown("---")
    name_cols = st.columns([2, 2, 1])
    prod_name = name_cols[0].text_input("Product Name", key=f"prod_name_{i}")
    emoji_choice = name_cols[1].selectbox("Product Icon", list(emoji_options.keys()), index=list(emoji_options.keys()).index(st.session_state.get(f"emoji_{i}", "🛒 Default")), key=f"emoji_{i}")
    emoji = emoji_options[emoji_choice]
    display_name = f"{emoji} {prod_name.strip()}" if prod_name.strip() else f"🆕 Product #{i+1}"

    st.subheader(display_name)

    cols = st.columns(1 + num_competitors + 1)
    your_price = cols[0].number_input("Your Price", 0.0, step=0.01, key=f"your_price_{i}")
    competitor_prices = []
    for j in range(num_competitors):
        cp = cols[j+1].number_input(competitor_names[j], 0.0, step=0.01, key=f"comp_{j}_{i}")
        competitor_prices.append(cp)

    valid_prices = [p for p in competitor_prices if p > 0]
    lowest = min(valid_prices) if valid_prices else 0.0
    floor = round(your_price * (floor_percent / 100), 2)
    suggested = max(round(lowest - undercut_amount, 2), floor) if lowest > 0 else 0.0
    hit_floor = suggested == floor and suggested > 0

    color = "red" if hit_floor else "lime"
    icon = "🔒" if hit_floor else "💡"
    cols[-1].markdown(f"""
    <div style='line-height:1.3'>
        <span style='font-size: 18px;'>{icon} <strong>Suggested:</strong> 
        <span style='color:{color};'>${suggested:.2f}</span></span><br>
        <small><em>Floor: ${floor:.2f}, Undercut: ${undercut_amount:.2f}</em></small>
    </div>
    """, unsafe_allow_html=True)

    row = {
        "Product": display_name,
        "Your Price": your_price,
        "Lowest Competitor": lowest,
        "Suggested Price": suggested,
        "Price Floor (%)": f"{floor_percent}%",
        "Price Floor Value": floor,
        "Hit Floor": hit_floor
    }
    for j in range(num_competitors):
        row[competitor_names[j]] = competitor_prices[j]

    ui_data.append(row)
    export_row = row.copy()
    export_row["Product"] = prod_name or f"Product {i+1}"
    excel_data.append(export_row)

# -----------------------------
# Final Table
# -----------------------------
st.markdown("## 📊 Suggested Prices Table")
df_ui = pd.DataFrame(ui_data)
st.dataframe(df_ui, use_container_width=True)

# -----------------------------
# Excel Export
# -----------------------------
df_export = pd.DataFrame(excel_data)
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df_export.to_excel(writer, index=False, sheet_name="Repricing")
    writer.sheets["Repricing"].set_column("A:Z", 18)

st.download_button(
    "📥 Download as Excel (.xlsx)",
    data=output.getvalue(),
    file_name="repricing_suggestions.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
