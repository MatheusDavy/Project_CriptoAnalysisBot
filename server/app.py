import os
import time
import logging
import threading
import pandas as pd
import matplotlib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from utils.limit import calculate_limit

matplotlib.use('Agg')

from settings import SYMBOL, TIMEFRAME, LIMIT, UPDATE_INTERVAL_SECONDS, CHART_PATH
from core.exchange import fetch_ohlcv
from core.analysis import apply_technical_analysis
from core.signals import generate_signals
from core.chart import generate_chart

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app, support_credentials=True)

ohlcv_data = pd.DataFrame()
buy_signals = []
sell_signals = []

def update():
    global ohlcv_data, buy_signals, sell_signals
    ohlcv = fetch_ohlcv(SYMBOL, TIMEFRAME, limit=LIMIT)
    if ohlcv:
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = apply_technical_analysis(df)
        buy_signals, sell_signals = generate_signals(df)
        generate_chart(df, buy_signals, sell_signals, CHART_PATH)
        ohlcv_data = df

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analysis')
def get_data():
    symbol = request.args.get("symbol", "BTCUSDT")
    interval = request.args.get("interval", "1m")
    months = int(request.args.get("months", 1))
    limit = calculate_limit(interval, months)

    candles = fetch_ohlcv(symbol, interval, limit)

    return jsonify({
        "candles": candles
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)