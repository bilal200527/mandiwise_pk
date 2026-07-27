import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# Page Setup
st.set_page_config(page_title="MandiWise PK - Agri Market Advisor", page_icon="🌾", layout="wide")
st.title("🌾 MandiWise PK — Agri-Wholesale Price Intelligence")
st.caption("Real-time market rates and AI trade advisory for Pakistani farmers and vendors.")

# Simulated Live Wholesale Rates (PKR per Kg) based on current averages
data = {
    "City": ["Lahore", "Karachi", "Multan", "Faisalabad"] * 4,
    "Crop": ["Tomato"]*4 + ["Onion"]*4 + ["Wheat"]*4 + ["Cotton (Phutti)"]*4,
    "Price_PKR": [
        180, 210, 150, 165,  # Tomato
        85, 95, 70, 75,      # Onion
        85, 90, 80, 82,      # Wheat
        240, 245, 238, 240   # Cotton
    ]
}
df = pd.DataFrame(data)

# Sidebar UI
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Groq API Key:", type="password", help="Required for the AI Advisor")
    st.markdown("---")
    st.header("📋 Trade Details")
    selected_crop = st.selectbox("Select Crop", df['Crop'].unique())
    user_city = st.selectbox("Your Current City", df['City'].unique())
    quantity_kg = st.number_input("Total Quantity (Kg)", min_value=100, value=1000, step=100)
    transport_cost = st.number_input("Transport Cost to other cities (PKR per Kg)", min_value=1, value=15)
    analyze_btn = st.button("🚀 Analyze Market & Get AI Advice", type="primary", use_container_width=True)

# Main Dashboard
st.subheader(f"📊 Current Wholesale Market Trends for {selected_crop}")

# Filter data for selected crop
crop_data = df[df['Crop'] == selected_crop].sort_values(by="Price_PKR", ascending=False)
local_price = crop_data[crop_data['City'] == user_city]['Price_PKR'].values[0]
max_price_city = crop_data.iloc[0]['City']
max_price = crop_data.iloc[0]['Price_PKR']

# Render Interactive Plotly Chart
fig = px.bar(
    crop_data, 
    x='City', 
    y='Price_PKR', 
    color='City',
    title=f"{selected_crop} Prices Across Major Mandis (PKR/Kg)",
    text_auto=True
)
st.plotly_chart(fig, use_container_width=True)

# AI Advisory Section
if analyze_btn:
    if not api_key:
        st.error("⚠️ Please enter your Groq API Key in the sidebar.")
    else:
        with st.spinner("🤖 AI Market Advisor is analyzing routes and profitability..."):
            client = Groq(api_key=api_key)
            
            system_prompt = """
            You are 'Kisaan AI', an expert agricultural economist and commodity advisor in Pakistan. 
            You speak directly to local farmers and traders using a highly professional yet accessible tone. Use a mix of English and brief, natural Roman Urdu phrases where appropriate (e.g., 'Munafa', 'Mandi', 'Fasal').
            
            Your job is to analyze the provided market prices, transport costs, and crop quantities to give explicit, actionable advice on whether the user should:
            1. Sell in their local city right now.
            2. Transport their goods to the highest-paying city.
            
            Structure your response using these exact markdown headers:
            ### 🧮 Profitability Breakdown
            (Calculate the math clearly: Total revenue locally vs. Total revenue if transported minus transport costs).
            
            ### ⚖️ Final Trade Verdict
            (Give a clear, definitive recommendation on what to do).
            
            ### 💡 Pro-Tip for this Crop
            (One specific piece of advice regarding the shelf-life or trading behavior of this specific crop).
            """
            
            user_prompt = f"""
            CROP: {selected_crop}
            QUANTITY: {quantity_kg} Kg
            MY LOCAL CITY: {user_city} (Local Price: {local_price} PKR/Kg)
            HIGHEST PAYING CITY: {max_price_city} (Price: {max_price} PKR/Kg)
            TRANSPORT COST TO OTHER CITY: {transport_cost} PKR/Kg
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3
                )
                
                st.success("✅ Market Analysis Complete!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error during API call: {str(e)}")
