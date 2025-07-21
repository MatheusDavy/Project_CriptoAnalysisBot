import logging
import pandas as pd
from core.candlestick import detect_candle_patterns

def calculate_bollinger_bands(df, window=20, num_std=2):
    """Calcula Bollinger Bands e adiciona ao df."""
    if 'close' not in df.columns:
        logging.warning("Coluna 'close' não encontrada para calcular Bollinger Bands.")
        return df # Retorna o DataFrame original se 'close' não estiver presente

    df['BB_Middle'] = df['close'].rolling(window=window, min_periods=1).mean() # min_periods para evitar NaN no início
    df['BB_Std'] = df['close'].rolling(window=window, min_periods=1).std()
    df['BB_Upper'] = df['BB_Middle'] + num_std * df['BB_Std']
    df['BB_Lower'] = df['BB_Middle'] - num_std * df['BB_Std']
    return df

def generate_signals(df):
    buy_signals_dates = [] # Renamed for clarity: storing dates/index
    sell_signals_dates = [] # Renamed for clarity: storing dates/index

    if df.empty:
        logging.warning("DataFrame vazio. Nenhum sinal gerado.")
        return buy_signals_dates, sell_signals_dates

    # Calcula Bollinger Bands (já dentro da função generate_signals)
    # Garante que 'close' existe antes de calcular BB
    if 'close' in df.columns:
        df = calculate_bollinger_bands(df)
    else:
        logging.warning("Coluna 'close' não encontrada. Bollinger Bands não calculadas.")

    # Inicializa flags de sinais para todas as colunas esperadas
    # Melhor forma de garantir que todas as colunas existem antes de atribuir False
    signal_cols = ['ma_buy', 'ma_sell', 'rsi_buy', 'rsi_sell', 'macd_buy', 'macd_sell',
                   'bb_buy', 'bb_sell', 'vol_buy', 'ml_buy', 'ml_sell', 'prophet_buy', 'prophet_sell',
                   'pattern_buy', 'pattern_sell'] # Adicionado pattern_buy/sell
    for col in signal_cols:
        if col not in df.columns:
            df[col] = False # Inicializa como False se não existir

    # --- Sinais Individuais ---

    # 1. SMA / EMA Cross
    if 'SMA_20' in df.columns and 'EMA_50' in df.columns:
        df['ma_buy'] = (df['SMA_20'].shift(1) < df['EMA_50'].shift(1)) & (df['SMA_20'] > df['EMA_50'])
        df['ma_sell'] = (df['SMA_20'].shift(1) > df['EMA_50'].shift(1)) & (df['SMA_20'] < df['EMA_50'])

    # 2. RSI 14
    if 'RSI_14' in df.columns:
        df['rsi_buy'] = df['RSI_14'] < 30
        df['rsi_sell'] = df['RSI_14'] > 70
        # Adição: Sinais de divergência ou RSI cruzando 50 podem ser mais poderosos
        # Ex: df['rsi_buy_cross_30'] = (df['RSI_14'].shift(1) < 30) & (df['RSI_14'] >= 30)

    # 3. MACD Cross
    if 'MACD_12_26_9' in df.columns and 'MACDs_12_26_9' in df.columns:
        macd_prev_diff = df['MACD_12_26_9'].shift(1) - df['MACDs_12_26_9'].shift(1)
        macd_now_diff = df['MACD_12_26_9'] - df['MACDs_12_26_9']
        df['macd_buy'] = (macd_prev_diff < 0) & (macd_now_diff > 0) # MACD cruza acima da linha de sinal
        df['macd_sell'] = (macd_prev_diff > 0) & (macd_now_diff < 0) # MACD cruza abaixo da linha de sinal

    # 4. Bollinger Bands - preço fecha abaixo da banda inferior → compra; acima da superior → venda
    if all(col in df.columns for col in ['close', 'BB_Upper', 'BB_Lower']):
        # Adicionando um pequeno atraso (shift) para evitar "look-ahead bias"
        # Isso garante que você só age no próximo candle após o sinal, como na vida real.
        df['bb_buy'] = (df['close'].shift(1) < df['BB_Lower'].shift(1)) # Sinal de compra no candle anterior
        df['bb_sell'] = (df['close'].shift(1) > df['BB_Upper'].shift(1)) # Sinal de venda no candle anterior
        # Alternativa: o sinal é gerado QUANDO o preço fecha fora, e a entrada ocorreria NO PRÓXIMO candle.
        # Sua lógica original: df['bb_buy'] = df['close'] < df['BB_Lower']
        # Se você está backtesting com dados de fechamento, essa é a forma correta para o momento do sinal.
        # Apenas considere como você está interpretando a entrada no backtest.

    # 5. Volume acima da média (últimos 20 candles)
    if 'volume' in df.columns:
        df['vol_ma'] = df['volume'].rolling(window=20, min_periods=1).mean()
        df['vol_buy'] = df['volume'] > 1.5 * df['vol_ma']
    else:
        logging.warning("Coluna 'volume' não encontrada. Sinais de volume não calculados.")
        df['vol_buy'] = False # Garante que a coluna existe

    # 6. Sinais de ML (pré-calculados externamente e injetados no DataFrame)
    if 'ml_buy' not in df.columns or 'ml_sell' not in df.columns:
        logging.warning("Sinais de ML não encontrados. 'ml_buy' e 'ml_sell' foram definidos como False.")
        df['ml_buy'] = False
        df['ml_sell'] = False
    else:
        df['ml_buy'] = df['ml_buy'].astype(bool)
        df['ml_sell'] = df['ml_sell'].astype(bool)

    # 7. Sinais de Prophet (pré-calculados externamente e injetados no DataFrame)
    if 'prophet_buy' not in df.columns or 'prophet_sell' not in df.columns:
        logging.warning("Sinais do Prophet não encontrados. 'prophet_buy' e 'prophet_sell' foram definidos como False.")
        df['prophet_buy'] = False
        df['prophet_sell'] = False
    else:
        df['prophet_buy'] = df['prophet_buy'].astype(bool)
        df['prophet_sell'] = df['prophet_sell'].astype(bool)

    # 8. Padrões de Candlestick
    # Garante que 'open', 'high', 'low', 'close' estão presentes
    if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        df = detect_candle_patterns(df) # Esta função deve adicionar 'pattern_buy' e 'pattern_sell'
    else:
        logging.warning("Colunas OHLC não encontradas. Padrões de candlestick não detectados.")
        df['pattern_buy'] = False
        df['pattern_sell'] = False

    # ======= CONFLUÊNCIA ATIVADA =======
    # Definindo um mínimo de confluências para um sinal forte
    # Você pode ajustar esses pesos ou o mínimo de confluências
    min_confluences_buy = 2 # Exemplo: 2 ou mais condições de compra verdadeiras
    min_confluences_sell = 2 # Exemplo: 2 ou mais condições de venda verdadeiras

    for i in range(len(df)): # Itera sobre o DataFrame
        # Garante que os índices existam (pode haver NaN no início devido a rolling windows/shifts)
        if i == 0 or any(pd.isna(df.iloc[i][col]) for col in ['BB_Upper', 'BB_Lower', 'SMA_20', 'EMA_50', 'RSI_14', 'MACD_12_26_9']):
            continue # Pula as primeiras linhas onde os indicadores não estão totalmente calculados

        # Soma das confluências de COMPRA
        confluences_buy_count = 0
        if df['ma_buy'].iloc[i]: confluences_buy_count += 1
        if df['macd_buy'].iloc[i]: confluences_buy_count += 1
        if df['bb_buy'].iloc[i]: confluences_buy_count += 1
        if df['vol_buy'].iloc[i]: confluences_buy_count += 1
        if df['ml_buy'].iloc[i]: confluences_buy_count += 1
        if df['prophet_buy'].iloc[i]: confluences_buy_count += 1
        if 'pattern_buy' in df.columns and df['pattern_buy'].iloc[i]: confluences_buy_count += 1


        # Soma das confluências de VENDA
        confluences_sell_count = 0
        if df['ma_sell'].iloc[i]: confluences_sell_count += 1
        if df['macd_sell'].iloc[i]: confluences_sell_count += 1
        if df['bb_sell'].iloc[i]: confluences_sell_count += 1
        if df['ml_sell'].iloc[i]: confluences_sell_count += 1
        if df['prophet_sell'].iloc[i]: confluences_sell_count += 1
        if 'pattern_sell' in df.columns and df['pattern_sell'].iloc[i]: confluences_sell_count += 1


        # Geração dos sinais finais de compra/venda
        if confluences_buy_count >= min_confluences_buy:
            # Adiciona uma condição para evitar sinais de compra enquanto já há sinal de venda forte e vice-versa
            if confluences_sell_count < min_confluences_sell: # Evita sinais conflitantes no mesmo candle
                buy_signals_dates.append(df.index[i])
                logging.debug(f"Sinal de COMPRA em {df.index[i]} com {confluences_buy_count} confluências.")
        elif confluences_sell_count >= min_confluences_sell:
            if confluences_buy_count < min_confluences_buy: # Evita sinais conflitantes no mesmo candle
                sell_signals_dates.append(df.index[i])
                logging.debug(f"Sinal de VENDA em {df.index[i]} com {confluences_sell_count} confluências.")

    logging.info(f"Sinais gerados: {len(buy_signals_dates)} compra(s), {len(sell_signals_dates)} venda(s)")
    return buy_signals_dates, sell_signals_dates