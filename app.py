import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import requests

# Function to fetch stock data from Yahoo Finance API
def get_stock_data(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1mo"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        result = data.get('chart', {}).get('result')
        if not result or 'timestamp' not in result[0] or 'indicators' not in result[0]:
            return None

        timestamps = result[0]['timestamp']
        prices = result[0]['indicators']['quote'][0]['close']

        if not timestamps or not prices:
            return None

        dates = pd.to_datetime(timestamps, unit='s')
        df = pd.DataFrame({'Date': dates, 'Close': prices})
        return df.dropna()

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Stock Market Dashboard", layout="centered")
st.title("📈 Real-Time Stock Market Dashboard")
st.write("Enter a stock symbol (e.g., AAPL, TSLA, INFY, TCS):")

# User input
symbol = st.text_input("Stock Symbol", "AAPL").strip().upper()

# Fetch and display data
if symbol:
    df = get_stock_data(symbol)

    if df is not None and not df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=symbol))
        fig.update_layout(
            title=f"{symbol} - Stock Price (Last 1 Month)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template='plotly_white'
        )
        st.plotly_chart(fig)
    else:
        st.error("⚠️ Could not fetch stock data. Please check the symbol or try again later.")
