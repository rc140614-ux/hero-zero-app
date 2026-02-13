import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Hero Zero Scanner", layout="wide")

st.title("🔥 Hero Zero NIFTY 50 Auto Scanner")
st.write("Rahul Edition 🚀")

nifty50 = [
    "RELIANCE.NS","HDFCBANK.NS","INFY.NS","TCS.NS","ICICIBANK.NS",
    "SBIN.NS","LT.NS","AXISBANK.NS","ITC.NS","BAJFINANCE.NS",
    "ASIANPAINT.NS","MARUTI.NS","HCLTECH.NS","SUNPHARMA.NS",
    "TITAN.NS","ULTRACEMCO.NS","NESTLEIND.NS","POWERGRID.NS",
    "KOTAKBANK.NS","NTPC.NS","ONGC.NS","TECHM.NS",
    "WIPRO.NS","INDUSINDBK.NS","JSWSTEEL.NS","TATAMOTORS.NS",
    "ADANIENT.NS","ADANIPORTS.NS","BAJAJFINSV.NS","BHARTIARTL.NS",
    "COALINDIA.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS",
    "HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS",
    "BPCL.NS","BRITANNIA.NS","CIPLA.NS","DIVISLAB.NS",
    "M&M.NS","SHREECEM.NS","SBILIFE.NS","TATASTEEL.NS",
    "UPL.NS","APOLLOHOSP.NS","BAJAJ-AUTO.NS","LTIM.NS"
]

results = []

scan_button = st.button("🔎 Scan NIFTY 50")

if scan_button:
    progress_bar = st.progress(0)

    for i, stock in enumerate(nifty50):
        try:
            data = yf.download(stock, interval="5m", period="5d", progress=False)

            if len(data) < 50:
                continue

            data['EMA9'] = ta.trend.ema_indicator(data['Close'], window=9)
            data['EMA21'] = ta.trend.ema_indicator(data['Close'], window=21)
            data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
            data['Volume_MA'] = data['Volume'].rolling(20).mean()

            latest = data.iloc[-1]

            if (latest['EMA9'] > latest['EMA21'] and 
                latest['RSI'] > 60 and 
                latest['Volume'] > latest['Volume_MA']):
                
                results.append([stock, "BUY 🚀"])

            elif (latest['EMA9'] < latest['EMA21'] and 
                  latest['RSI'] < 40 and 
                  latest['Volume'] > latest['Volume_MA']):
                
                results.append([stock, "SELL 🔻"])

        except:
            pass

        progress_bar.progress((i + 1) / len(nifty50))

    if results:
        df = pd.DataFrame(results, columns=["Stock", "Signal"])
        st.success("🔥 Hero Zero Setup Found")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Abhi kisi NIFTY 50 stock me clear Hero Zero setup nahi bana")
