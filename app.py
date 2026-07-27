import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# Page Setup
st.set_page_config(page_title="MandiWise PK - Agri Market Intelligence", page_icon="🌾", layout="wide")
st.title("🌾 MandiWise PK — Agri-Wholesale Price Intelligence")
st.caption("Real-time mandi rates, market arbitrage analytics, and AI trade advisory for Pakistani farmers and vendors.")

# 1. Expanded Realistic Pakistan Mandi Dataset
crops_data = {
    "Wheat (Gandum)": 88,
    "Basmati Rice": 240,
    "Cotton (Phutti)": 245,
    "Sugarcane": 12,
    "Maize (Makai)": 65,
    "Tomato": 180,
    "Onion": 85,
    "Potato": 60,
    "Mango (Chaunsa/Sindhri)": 220,
    "Citrus (Kinnow)": 140,
    "Red Chili": 450,
    "Garlic (Lehsan)": 380
}

cities_variance = {
    "Karachi": 1.18,
    "Lahore": 1.05,
    "Rawalpindi / Islamabad": 1.12,
    "Faisalabad": 0.98,
    "Multan": 0.92,
    "Peshawar": 1.15,
    "Quetta": 1.22,
    "Hyderabad": 1.08,
    "Gujranwala": 1.02,
    "Sargodha": 0.94,
    "Sahiwal": 0.90,
    "Sukkur": 0.96,
    "Rahim Yar Khan": 0.91,
    "Swat": 1.10
}

# Generate complete dataset dynamically
rows = []
for crop, base_price in crops_data.items():
    for city, mult in cities_variance.items():
        price = round(base_price * mult)
        rows.append({"City": city, "Crop": crop, "Price_PKR": price})

df = pd.DataFrame(rows)

# Sidebar Controls
with st.sidebar:
    st.header("📋 Trade Configuration")
    selected_crop = st.selectbox("Select Commodity / Crop", df['Crop'].unique())
    user_city = st.selectbox("Your Origin City / Mandi", df['City'].unique())
    quantity_kg = st.number_input("Total Harvest Quantity (Kg)", min_value=100, value=1000, step=100)
    transport_cost = st.number_input("Estimated Freight / Transport Cost (PKR per Kg)", min_value=0, value=12)
    analyze_btn = st.button("🚀 Run Market Analysis & AI Advisor", type="primary", use_container_width=True)

# Main Dashboard View
col_left, col_right = st.columns([2, 1])

crop_df = df[df['Crop'] == selected_crop].sort_values(by="Price_PKR", ascending=False)
local_price = crop_df[crop_df['City'] == user_city]['Price_PKR'].values[0]
local_total_revenue = local_price * quantity_kg

with col_left:
    st.subheader(f"📊 Market Price Comparison: {selected_crop} (PKR / Kg)")
    fig = px.bar(
        crop_df, 
        x='City', 
        y='Price_PKR', 
        color='Price_PKR',
        color_continuous_scale='Greens',
        title=f"Wholesale Rates Across 14 Pakistani Mandis",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("💡 Local Mandi Summary")
    st.metric(label=f"Current Rate in {user_city}", value=f"{local_price} PKR / Kg")
    st.metric(label="Estimated Local Gross Revenue", value=f"{local_total_revenue:,} PKR")

st.markdown("---")

# NEW FEATURE: Arbitrage & Multi-Mandi Profit Ranking Table
st.subheader("⚡ NEW FEATURE: Multi-Mandi Arbitrage & Net Profit Matrix")
st.caption("Calculates net earnings across all mandis after subtracting freight costs from your origin city.")

arbitrage_df = crop_df.copy()
arbitrage_df['Gross_Revenue_PKR'] = arbitrage_df['Price_PKR'] * quantity_kg
arbitrage_df['Freight_Cost_PKR'] = arbitrage_df['City'].apply(lambda c: 0 if c == user_city else transport_cost * quantity_kg)
arbitrage_df['Net_Profit_PKR'] = arbitrage_df['Gross_Revenue_PKR'] - arbitrage_df['Freight_Cost_PKR']
arbitrage_df['Profit_Gain_vs_Local'] = arbitrage_df['Net_Profit_PKR'] - local_total_revenue

# Sort by highest net profit
arbitrage_df = arbitrage_df.sort_values(by="Net_Profit_PKR", ascending=False).reset_index(drop=True)

st.dataframe(
    arbitrage_df[['City', 'Price_PKR', 'Gross_Revenue_PKR', 'Freight_Cost_PKR', 'Net_Profit_PKR', 'Profit_Gain_vs_Local']],
    column_config={
        "City": "Destination Mandi",
        "Price_PKR": "Rate (PKR/Kg)",
        "Gross_Revenue_PKR": st.column_config.NumberColumn("Gross Revenue (PKR)", format="%d"),
        "Freight_Cost_PKR": st.column_config.NumberColumn("Freight Deduction (PKR)", format="%d"),
        "Net_Profit_PKR": st.column_config.NumberColumn("Net Earnings (PKR)", format="%d"),
        "Profit_Gain_vs_Local": st.column_config.NumberColumn("Extra Profit vs Local (PKR)", format="%d"),
    },
    use_container_width=True
)

best_city = arbitrage_df.iloc[0]['City']
best_extra_profit = arbitrage_df.iloc[0]['Profit_Gain_vs_Local']

if best_city != user_city and best_extra_profit > 0:
    st.success(f"🔥 **Arbitrage Opportunity:** Shipping to **{best_city}** yields an extra **{best_extra_profit:,} PKR** net profit after freight costs!")
else:
    st.info(f"ℹ️ **Local Advantage:** Selling locally in **{user_city}** is currently your most profitable option after factoring in transport fees.")

# AI Market Advisor Section
if analyze_btn:
    st.markdown("---")
    st.subheader("🤖 Kisaan AI Market Advisor Report")
    
    with st.spinner("Analyzing mandi supply trends and generating strategy..."):
        try:
            # Pulling key securely from Streamlit Secrets
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            system_prompt = """
            You are 'Kisaan AI', an expert agricultural economist and mandi trade strategist in Pakistan. 
            Provide clear, realistic advisory for farmers and traders. Blend professional English with natural Roman Urdu trade terms (e.g., 'Munafa', 'Mandi', 'Fasal', 'Ahti').
            
            Structure output strictly with these markdown headers:
            ### 🧮 Profitability & Freight Breakdown
            ### ⚖️ Final Trade Recommendation
            ### 💡 Storage & Quality Management Tip
            """
            
            user_prompt = f"""
            COMMODITY: {selected_crop}
            HARVEST VOLUME: {quantity_kg} Kg
            ORIGIN CITY: {user_city} (Price: {local_price} PKR/Kg)
            TOP DESTINATION MANDI: {best_city} (Price: {arbitrage_df.iloc[0]['Price_PKR']} PKR/Kg)
            FREIGHT COST: {transport_cost} PKR/Kg
            PROJECTED EXTRA PROFIT: {best_extra_profit} PKR
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error accessing Groq AI Advisor: {str(e)}. Make sure 'GROQ_API_KEY' is added to Streamlit Secrets.")
