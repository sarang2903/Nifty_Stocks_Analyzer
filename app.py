import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="📈 Nifty Stocks SMA Dashboard", layout="wide")

# --- Load Data ---
df = pd.read_csv("Stocks_2025.csv")
df = df.drop('Unnamed: 0', axis=1)
df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
df['Date'] = pd.to_datetime(df['Date'])
df['Stock'] = df['Stock'].replace(" ", "", regex=True)

# --- Title ---
st.title("📊 Nifty Stocks SMA (50 & 200) Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Category Selection
categories = sorted(df["Category"].unique())
selected_category = st.sidebar.selectbox("Select Category:", categories)

filtered_category = df[df["Category"] == selected_category]

# Stock Selection
stocks = sorted(filtered_category["Stock"].unique())
selected_stock = st.sidebar.selectbox("Select Stock:", stocks)

# Filter final data
selected_data = filtered_category[filtered_category["Stock"] == selected_stock]

# --- Display Data ---
with st.expander("📂 View Raw Data"):
    st.dataframe(selected_data.tail(20))

# --- Line Chart ---
st.subheader(f"📈 Stock Trend for {selected_stock} ({selected_category})")

fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(x=selected_data["Date"], y=selected_data["Close"], color='green', label='Close', ax=ax, marker='o')
sb.lineplot(x=selected_data["Date"], y=selected_data["SMA_50"], color='blue', label='SMA 50', ax=ax)
sb.lineplot(x=selected_data["Date"], y=selected_data["SMA_200"], color='red', label='SMA 200', ax=ax)

plt.title(f"{selected_stock} - Closing Price with SMA 50 & SMA 200", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
st.pyplot(fig)

# --- Insights Section ---
st.markdown("---")
st.markdown("### 💡 Quick Insights")

latest_close = selected_data["Close"].iloc[-1]
latest_sma50 = selected_data["SMA_50"].iloc[-1]
latest_sma200 = selected_data["SMA_200"].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("📉 Latest Close", f"₹{latest_close:.2f}")
col2.metric("📘 SMA 50", f"₹{latest_sma50:.2f}")
col3.metric("📕 SMA 200", f"₹{latest_sma200:.2f}")

# Trend Signal
if latest_sma50 > latest_sma200:
    st.success("✅ **Bullish Signal** — SMA 50 crossed above SMA 200 (Golden Cross)")
else:
    st.error("⚠️ **Bearish Signal** — SMA 50 below SMA 200 (Death Cross)")
