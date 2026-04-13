import time
import requests
from datetime import datetime

BASE = "https://fapi.binance.com"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "DOGEUSDT", "1000PEPEUSDT"]

# ====== 数据获取 ======
def get_oi(symbol):
    url = f"{BASE}/futures/data/openInterestHist"
    params = {"symbol": symbol, "period": "5m", "limit": 2}
    return requests.get(url, params=params).json()

def get_funding(symbol):
    url = f"{BASE}/fapi/v1/fundingRate"
    return requests.get(url, params={"symbol": symbol, "limit": 1}).json()

# ====== 信号系统 ======
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
print("=== 合约监控启动 ===")

while True:
    print("\n" + "="*50)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for s in SYMBOLS:
        try:
            oi_data = get_oi(s)
            funding_data = get_funding(s)

            # OI变化（简化稳定版）
            oi_old = float(oi_data[0]["sumOpenInterest"])
            oi_new = float(oi_data[-1]["sumOpenInterest"])
            oi_change = ((oi_new - oi_old) / oi_old) * 100

            funding = float(funding_data[0]["fundingRate"])

            sig = signal(oi_change, funding)

            print(f"{s} | OI变化: {oi_change:.2f}% | Funding: {funding:.5f} | 信号: {sig}")

        except Exception as e:
            print(f"{s} error:", e)

    time.sleep(60)
