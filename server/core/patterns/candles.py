import pandas as pd

# Engulfing
def engulfing(df):
    df['engulfing'] = 0
    for i in range(1, len(df)):
        prev, curr = df.iloc[i-1], df.iloc[i]
        if (prev['close'] < prev['open'] and curr['open'] < curr['close'] and curr['open'] < prev['close'] and curr['close'] > prev['open']):
            df.at[df.index[i], 'engulfing'] = 1  # Bullish
        elif (prev['close'] > prev['open'] and curr['open'] > curr['close'] and curr['open'] > prev['close'] and curr['close'] < prev['open']):
            df.at[df.index[i], 'engulfing'] = -1  # Bearish
    return df

# Hammer
def hammer(df):
    df['hammer'] = 0
    for i in range(len(df)):
        c = df.iloc[i]
        body = abs(c['close'] - c['open'])
        lower_wick = min(c['open'], c['close']) - c['low']
        upper_wick = c['high'] - max(c['open'], c['close'])
        if lower_wick > 2 * body and upper_wick < body:
            df.at[df.index[i], 'hammer'] = 1
    return df

# Doji
def doji(df):
    df['doji'] = 0
    for i in range(len(df)):
        c = df.iloc[i]
        body = abs(c['close'] - c['open'])
        total_range = c['high'] - c['low']
        if total_range > 0 and body < 0.1 * total_range:
            df.at[df.index[i], 'doji'] = 1
    return df

# Morning Star
def morning_star(df):
    df['morning_star'] = 0
    for i in range(2, len(df)):
        c1, c2, c3 = df.iloc[i-2], df.iloc[i-1], df.iloc[i]
        # Condição 1: Primeiro candle de baixa (corpo grande)
        bearish_c1 = c1['close'] < c1['open'] and (c1['open'] - c1['close']) > (c1['high'] - c1['low']) * 0.6
        # Condição 2: Segundo candle pequeno (doji ou corpo pequeno), idealmente gap down
        small_body_c2 = abs(c2['close'] - c2['open']) < (c2['high'] - c2['low']) * 0.3
        gap_down_c2 = c2['high'] < c1['close']
        # Condição 3: Terceiro candle de alta (corpo grande) fechando acima do ponto médio do primeiro
        bullish_c3 = c3['close'] > c3['open'] and (c3['close'] - c3['open']) > (c3['high'] - c3['low']) * 0.6
        close_above_mid_c1 = c3['close'] > (c1['open'] + c1['close']) / 2

        if bearish_c1 and small_body_c2 and gap_down_c2 and bullish_c3 and close_above_mid_c1:
            df.at[df.index[i], 'morning_star'] = 1
    return df

# Evening Star
def evening_star(df):
    df['evening_star'] = 0
    for i in range(2, len(df)):
        c1, c2, c3 = df.iloc[i-2], df.iloc[i-1], df.iloc[i]
        # Condição 1: Primeiro candle de alta (corpo grande)
        bullish_c1 = c1['close'] > c1['open'] and (c1['close'] - c1['open']) > (c1['high'] - c1['low']) * 0.6
        # Condição 2: Segundo candle pequeno (doji ou corpo pequeno), idealmente gap up
        small_body_c2 = abs(c2['close'] - c2['open']) < (c2['high'] - c2['low']) * 0.3
        gap_up_c2 = c2['low'] > c1['close']
        # Condição 3: Terceiro candle de baixa (corpo grande) fechando abaixo do ponto médio do primeiro
        bearish_c3 = c3['close'] < c3['open'] and (c3['open'] - c3['close']) > (c3['high'] - c3['low']) * 0.6
        close_below_mid_c1 = c3['close'] < (c1['open'] + c1['close']) / 2

        if bullish_c1 and small_body_c2 and gap_up_c2 and bearish_c3 and close_below_mid_c1:
            df.at[df.index[i], 'evening_star'] = -1
    return df

# Harami
def harami(df):
    df['harami'] = 0
    for i in range(1, len(df)):
        prev, curr = df.iloc[i-1], df.iloc[i]
        # Bullish Harami: Grande candle de baixa seguido por pequeno candle de alta contido no corpo do anterior
        if (prev['close'] < prev['open'] and  # Previous candle is bearish
            curr['open'] < curr['close'] and  # Current candle is bullish
            curr['low'] > prev['close'] and  # Current candle's low is above previous close (within body)
            curr['high'] < prev['open'] and  # Current candle's high is below previous open (within body)
            abs(prev['close'] - prev['open']) > 2 * abs(curr['close'] - curr['open'])): # Previous body is much larger
            df.at[df.index[i], 'harami'] = 1  # Bullish Harami
        # Bearish Harami: Grande candle de alta seguido por pequeno candle de baixa contido no corpo do anterior
        elif (prev['close'] > prev['open'] and  # Previous candle is bullish
              curr['open'] > curr['close'] and  # Current candle is bearish
              curr['low'] > prev['open'] and  # Current candle's low is above previous open (within body)
              curr['high'] < prev['close'] and  # Current candle's high is below previous close (within body)
              abs(prev['close'] - prev['open']) > 2 * abs(curr['close'] - curr['open'])): # Previous body is much larger
            df.at[df.index[i], 'harami'] = -1 # Bearish Harami
    return df

# Inverted Hammer
def inverted_hammer(df):
    df['inverted_hammer'] = 0
    for i in range(len(df)):
        c = df.iloc[i]
        body = abs(c['close'] - c['open'])
        upper_wick = c['high'] - max(c['open'], c['close'])
        lower_wick = min(c['open'], c['close']) - c['low']
        # Condições para Inverted Hammer: corpo pequeno, sombra superior longa, sombra inferior pequena/inexistente
        if upper_wick > 2 * body and lower_wick < body and body > 0:
            df.at[df.index[i], 'inverted_hammer'] = 1
    return df

# Detectar padrões
def detect_candle_signals(df):
    df = engulfing(df)
    df = hammer(df)
    df = doji(df)
    df = morning_star(df)
    df = evening_star(df)
    df = harami(df)
    df = inverted_hammer(df)

    df['candles_buy'] = (df['engulfing'] == 1) | \
                        (df['hammer'] == 1) | \
                        (df['morning_star'] == 1) | \
                        (df['harami'] == 1) | \
                        (df['inverted_hammer'] == 1)

    df['candles_sell'] = (df['engulfing'] == 1) | \
                         (df['evening_star'] == 1) | \
                         (df['harami'] == 1)
    return df