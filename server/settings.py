import os
from dotenv import load_dotenv
from utils.limit import calculate_limit

load_dotenv()

SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1h")
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance")
TIMERANGE = int(os.getenv("TIMERANGE", "1"))  # converte para int aqui
LIMIT = calculate_limit(TIMEFRAME, TIMERANGE)
UPDATE_INTERVAL_SECONDS = int(os.getenv("UPDATE_INTERVAL_SECONDS", 300))
CHART_PATH = "static/candlestick_chart.png"