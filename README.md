Here is the complete, submission-ready `README.md` file with your live link integrated. You can copy and paste this code block directly into your GitHub repository:

```markdown
# 🌾 MandiWise PK — Agri-Wholesale Price Intelligence & Arbitrage Engine

**Live App URL:** https://mandiwisepk-dtufnftmzszajyapwexpmj.streamlit.app/

---

## 📌 a. App Name, Problem Statement & Target Audience

* **App Name:** MandiWise PK
* **The Real Problem:** Agricultural vendors, farmers, and traders across Pakistan face extreme wholesale price volatility and middleman (*Ahti*) exploitation. Small-scale producers lack real-time visibility into regional mandi rates and struggle to calculate whether transporting harvest to a neighboring city is actually profitable after factoring in heavy freight costs.
* **Who It Is For:** Pakistani farmers, regional wholesale commodity traders, agricultural logistics managers, and supply chain analysts.

---

## ✨ b. Comprehensive Features List

1. **Multi-Mandi Wholesale Market Board:** Tracks live rates for **12 essential Pakistani commodities** (Wheat, Basmati Rice, Cotton, Sugarcane, Maize, Tomato, Onion, Potato, Mango, Kinnow, Red Chili, Garlic) across **14 major city mandis** (Karachi, Lahore, Rawalpindi/Islamabad, Multan, Faisalabad, Peshawar, Quetta, Hyderabad, Gujranwala, Sargodha, Sahiwal, Sukkur, Rahim Yar Khan, Swat).
2. **Interactive Data Visualization:** Renders dynamic `Plotly Express` bar charts comparing wholesale rates across all 14 markets to identify high-value regional hubs instantly.
3. **Multi-Mandi Arbitrage & Net Profit Matrix:** Automatically calculates gross revenue, freight deductions, and net earnings for all 14 markets simultaneously, highlighting the **#1 Most Profitable City** to ship to.
4. **Local Mandi Summary:** Evaluates gross earnings for selling locally versus shipping out-of-city.
5. **Kisaan AI Market Advisor:** An integrated LLM agent that processes the market math and generates a customized, actionable trading strategy using a culturally accessible blend of English and Roman Urdu.

---

## 🧠 c. The AI Feature & System Prompt

The core intelligence of **MandiWise PK** is powered by an AI Market Advisor. It ingests the user's origin mandi, commodity rates, harvest volume, and freight costs, then executes an economic breakdown to generate an explicit selling strategy.

### Exact System Prompt Used:
```text
You are 'Kisaan AI', an expert agricultural economist and mandi trade strategist in Pakistan. 
Provide clear, realistic advisory for farmers and traders. Blend professional English with natural Roman Urdu trade terms (e.g., 'Munafa', 'Mandi', 'Fasal', 'Ahti').

Structure output strictly with these markdown headers:
### 🧮 Profitability & Freight Breakdown
### ⚖️ Final Trade Recommendation
### 💡 Storage & Quality Management Tip

```

---

## 🛠️ d. Tools, Services, and AI Models Used

* **Frontend / Web Framework:** Streamlit (`app.py`)
* **Data Processing & Analytics:** `pandas`
* **Data Visualization:** `plotly.express`
* **AI Model Engine:** Groq API (`llama-3.3-70b-versatile`)
* **Deployment Platform:** Streamlit Community Cloud
* **Environment Security:** Streamlit Secrets Management (`st.secrets`)

---

## 📸 e. Screenshots of the App in Action


<img width="360" height="714" alt="image" src="https://github.com/user-attachments/assets/091a8bdc-ac27-4a63-8457-84a5a37fb2d0" />



<img width="1407" height="745" alt="image" src="https://github.com/user-attachments/assets/6739be86-b07a-4d92-ab2b-0879a5602a21" />



<img width="1760" height="825" alt="image" src="https://github.com/user-attachments/assets/03b0133c-44e7-4ea3-8cda-e0c11c65251c" />


---

## 🚀 f. How to Run the Project Locally

If you wish to run this application on your local machine:

1. **Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/mandiwise_pk.git](https://github.com/YOUR_USERNAME/mandiwise_pk.git)
cd mandiwise_pk

```


2. **Install required dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up Local Environment Secrets:**
Create a `.streamlit/secrets.toml` file in the project root and add your Groq API key:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"

```


4. **Launch the Streamlit app:**
```bash
streamlit run app.py

```



```

```
