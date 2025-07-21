import requests

def fetch_ohlcv(symbol, interval, limit=100):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "timestamp": int(k[0]),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5])
            }
            for k in data
        ]
    except Exception as e:
        print(f"[fetch_ohlcv] Erro ao buscar dados da Binance: {e}")
        return []
