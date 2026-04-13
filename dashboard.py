import time
import requests
from datetime import datetime

# ====== 填你的TG信息 ======
BOT_TOKEN = "8611767757:AAHLiJlDIv2jaq6Sys78z37_aDXUwWKaZwE"
CHAT_ID = "8166795654"

BASE = "https://fapi.binance.com"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "DOGEUSDT", "1000PEPEUSDT"]

# ====== TG发送 ======
def send_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

# ====== 数据 ======
def get_oi(symbol):
    url = f"{BASE}/futures/data/openInterestHist"
    return requests.get(url, params={"symbol": symbol, "period": "5m", "limit": 2}).json()

def get_funding(symbol):
    url = f"{BASE}/fapi/v1/fundingRate"
    return requests.get(url, params={"symbol": symbol, "limit": 1}).json()

# ====== 信号 ======
def signal(oi_change, funding):
    score = 0

    if oi_change > 8:
        score += 2

    if abs(funding) > 0.01:
        score += 2

    if score >= 4:
        return "🔥 STRONG"
    elif score == 2:
        return "⚠️ MEDIUM"
    else:
        return "🟢 WEAK"

# ====== 主循环 ======
send_tg("✅ 合约监控已启动")

while True:
    for s in SYMBOLS:
        try:
            oi_data = get_oi(s)
            funding_data = get_funding(s)

            oi_old = float(oi_data[0]["sumOpenInterest"])
            oi_new = float(oi_data[-1]["sumOpenInterest"])
            oi_change = ((oi_new - oi_old) / oi_old) * 100

            funding = float(funding_data[0]["fundingRate"])

            sig = signal(oi_change, funding)

            if sig != "🟢 WEAK":
                msg = f"""
🚨 {s}
信号: {sig}
OI变化: {oi_change:.2f}%
Funding: {funding:.5f}
时间: {datetime.now().strftime('%H:%M:%S')}
"""
                send_tg(msg)

            print(s, sig)

        except Exception as e:
            print("error:", e)

    time.sleep(60)
