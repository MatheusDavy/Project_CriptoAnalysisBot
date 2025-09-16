import logging
import pandas as pd

from core.patterns.candles import detect_candle_signals
from core.patterns.indicators import bollinger_bands, ema_crossover, rsi_signal, macd, stochastic

from core.patterns.shapes.sr_levels import detect_support_resistance_signals
from core.patterns.shapes.hs import detect_hs_signals
from core.patterns.shapes.flags import detect_flag_signals
from core.patterns.shapes.fibonacci import generate_fibonacci_signals

from core.evaluate import evaluate_signals

def generate_signals(candles, analysis):
    min_conf_buy = analysis['confluence']['buy']
    min_conf_sell = analysis['confluence']['sell']

    df = pd.DataFrame(candles)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)

    # Análises ativadas
    if analysis['candles']:
        df = detect_candle_signals(df)

    if analysis['shapes']['sr']:
        df = detect_support_resistance_signals(df)

    if analysis['shapes']['flags']:
        df = detect_flag_signals(df)
    
    if analysis['shapes']['fibonacci']:
        df = generate_fibonacci_signals(df)

    if analysis['shapes']['hs']:
        df = detect_hs_signals(df)

    if analysis['indicators']['bb']:
        df = bollinger_bands(df)

    if analysis['indicators']['ema']:
        df = ema_crossover(df)

    if analysis['indicators']['rsi']:
        df = rsi_signal(df)

    if analysis['indicators']['macd']:
        df = macd(df)

    if analysis['indicators']['stochastic']:
        df = stochastic(df)

    # Lista temporária de sinais brutos
    buy_signals = []
    sell_signals = []

    for i in range(len(df) - 1):
        row = df.iloc[i]

        conf_buy = 0
        conf_sell = 0

        # Candles
        if analysis['candles']:
            conf_buy += int(row.get('candles_buy', False))
            conf_sell += int(row.get('candles_sell', False))

        # Shapes
        if analysis['shapes']['sr']:
            conf_buy += int(row.get('sr_buy', False))
            conf_sell += int(row.get('sr_sell', False))

        if analysis['shapes']['flags']:
            conf_buy += int(row.get('flags_buy', False))
            conf_sell += int(row.get('flags_sell', False))

        if analysis['shapes']['hs']:
            conf_buy += int(row.get('hs_buy', False))
            conf_sell += int(row.get('hs_sell', False))

        if analysis['shapes']['fibonacci']:
            conf_buy += int(row.get('fibonacci_buy', False))
            conf_sell += int(row.get('fibonacci_sell', False))

        # Indicadores
        if analysis['indicators']['bb']:
            conf_buy += int(row.get('bb_buy', False))
            conf_sell += int(row.get('bb_sell', False))

        if analysis['indicators']['ema']:
            conf_buy += int(row.get('ema_buy', False))
            conf_sell += int(row.get('ema_sell', False))

        if analysis['indicators']['rsi']:
            conf_buy += int(row.get('rsi_buy', False))
            conf_sell += int(row.get('rsi_sell', False))

        if analysis['indicators']['macd']:
            conf_buy += int(row.get('macd_buy', False))
            conf_sell += int(row.get('macd_sell', False))

        if analysis['indicators']['stochastic']:
            conf_buy += int(row.get('stoch_buy', False))
            conf_sell += int(row.get('stoch_sell', False))

        next_ts = df.index[i + 1]

        if conf_buy >= min_conf_buy and conf_sell < min_conf_sell:
            buy_signals.append(int(next_ts.timestamp()))

        elif conf_sell >= min_conf_sell and conf_buy < min_conf_buy:
            sell_signals.append(int(next_ts.timestamp()))

    # 🎯 Filtrando com modelo (apenas sinais > 70% de probabilidade de acerto)
    logging.info(f"[SINAIS] Sinais aceitos: {len(buy_signals)} compras | {len(sell_signals)} vendas")

    # Avaliação
    buy_eval = evaluate_signals(df, buy_signals, direction='buy', future_candles=10)
    sell_eval = evaluate_signals(df, sell_signals, direction='sell', future_candles=10)

    return buy_signals, sell_signals, buy_eval, sell_eval
