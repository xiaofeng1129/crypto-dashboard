import streamlit as st
import pandas as pd
import requests

BASE_URL = "https://fapi.binance.com"

st.title("📊 合约妖币监控系统 V2")

def get_data():
    return requests.get(BASE_URL + "/fapi/v1/ticker/24hr").json()

data = get_data()

rows = []

for t in data:
    if "USDT" not in t['symbol']:
        continue

    try:
        rows.append({
            "symbol": t['symbol'],
            "price_change%": float(t['priceChangePercent']),
            "volume": float(t['quoteVolume'])
        })
    except:
        continue

df = pd.DataFrame(rows)
df = df.sort_values("price_change%", ascending=False)

st.subheader("🔥 涨幅榜")
st.dataframe(df.head(20))

st.subheader("📉 跌幅榜")
st.dataframe(df.tail(20))
