import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from utils.limit import calculate_limit

import sys
sys.dont_write_bytecode = True

from core.exchange import fetch_ohlcv
from core.signals import generate_signals
from core.shapes import generate_shapes
from core.analysis import generate_analysis

app = Flask(__name__)
CORS(app, support_credentials=True)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analysis', methods=['POST'])
def get_data():
    data = request.get_json()
    print("JSON parseado:", data)

    symbol = data.get("symbol")
    timeframe = data.get("timeframe")
    timerange = int(data.get("timerange", 1))
    analysis = data.get("analysis", {})

    limit = calculate_limit(timeframe, timerange)
    candles = fetch_ohlcv(symbol, timeframe, limit)

    shapes, buy, sell, buy_eval, sell_eval = generate_analysis(candles, analysis)

    return jsonify({
        "candles": candles,
        "sell": sell,
        "buy": buy,
        "shapes": shapes,
        "evaluate": {
            "buy": buy_eval,
            "sell": sell_eval
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)