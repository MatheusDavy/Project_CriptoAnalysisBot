import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from dataclasses import dataclass
from typing import Dict, List, Tuple

from utils.perceptually_important import find_pips
from utils.rolling_window import rw_top, rw_bottom
from utils.trendline_automation import fit_trendlines_single

@dataclass
class FlagPattern:
    base_x: int         # Start of the trend index, base of pole
    base_y: float       # Start of trend price

    tip_x: int   = -1       # Tip of pole, start of flag
    tip_y: float = -1.

    conf_x: int   = -1      # Index where pattern is confirmed
    conf_y: float = -1.      # Price where pattern is confirmed

    pennant: bool = False      # True if pennant, false if flag

    flag_width: int    = -1
    flag_height: float = -1.

    pole_width: int    = -1
    pole_height: float = -1.

    # Upper and lower lines for flag, intercept is tip_x
    support_intercept: float = -1.
    support_slope: float = -1.
    resist_intercept: float = -1.
    resist_slope: float = -1.

# Pips
def check_bear_pattern_pips(pending: FlagPattern, data: np.array, i:int, order:int):
    
    # Find max price since local bottom, (top of pole)
    data_slice = data[pending.base_x: i + 1] # i + 1 includes current price
    min_i = data_slice.argmin() + pending.base_x # Min index since local top
    
    if i - min_i < max(5, order * 0.5): # Far enough from max to draw potential flag/pennant
        return False
    
    # Test flag width / height 
    pole_width = min_i - pending.base_x
    flag_width = i - min_i
    if flag_width > pole_width * 0.5: # Flag should be less than half the width of pole
        return False

    pole_height = pending.base_y - data[min_i] 
    flag_height = data[min_i:i+1].max() - data[min_i] 
    if flag_height > pole_height * 0.5: # Flag should smaller vertically than preceding trend
        return False

    # If here width/height are OK.
    
    # Find perceptually important points from pole to current time
    pips_x, pips_y = find_pips(data[min_i:i+1], 5, 3) # Finds pips between max and current index (inclusive)

    # Check center pip is less than two adjacent. /\/\ 
    if not (pips_y[2] < pips_y[1] and pips_y[2] < pips_y[3]):
        return False
    
    # Find slope and intercept of flag lines
    # intercept is at the max value (top of pole)
    support_rise = pips_y[2] - pips_y[0]
    support_run = pips_x[2] - pips_x[0]
    support_slope = support_rise / support_run
    support_intercept = pips_y[0] 

    resist_rise = pips_y[3] - pips_y[1]
    resist_run = pips_x[3] - pips_x[1]
    resist_slope = resist_rise / resist_run
    resist_intercept = pips_y[1] + (pips_x[0] - pips_x[1]) * resist_slope

    # Find x where two lines intersect.
    #print(pips_x[0], resist_slope, support_slope)
    if resist_slope != support_slope: # Not parallel
        intersection = (support_intercept - resist_intercept) / (resist_slope - support_slope)
        #print("Intersects at", intersection)
    else:
        intersection = -flag_width * 100

    # No intersection in flag area
    if intersection <= pips_x[4] and intersection >= 0:
        return False

    # Check if current point has a breakout of flag. (confirmation)
    support_endpoint = pips_y[0] + support_slope * pips_x[4]
    if pips_y[4] > support_endpoint:
        return False
    
    if resist_slope < 0:
        pending.pennant = True
    else:
        pending.pennant = False
    
    # Filter harshly diverging lines
    if intersection < 0 and intersection > -flag_width:
        return False

    pending.tip_x = min_i
    pending.tip_y = data[min_i]
    pending.conf_x = i
    pending.conf_y = data[i]
    pending.flag_width = flag_width
    pending.flag_height = flag_height
    pending.pole_width = pole_width
    pending.pole_height = pole_height
    pending.support_slope = support_slope
    pending.support_intercept = support_intercept
    pending.resist_slope = resist_slope
    pending.resist_intercept = resist_intercept
    

    return True

def check_bull_pattern_pips(pending: FlagPattern, data: np.array, i:int, order:int):
    
    # Find max price since local bottom, (top of pole)
    data_slice = data[pending.base_x: i + 1] # i + 1 includes current price
    max_i = data_slice.argmax() + pending.base_x # Max index since bottom
    pole_width = max_i - pending.base_x
    
    if i - max_i < max(5, order * 0.5): # Far enough from max to draw potential flag/pennant
        return False

    flag_width = i - max_i
    if flag_width > pole_width * 0.5: # Flag should be less than half the width of pole
        return False

    pole_height = data[max_i] - pending.base_y 
    flag_height = data[max_i] - data[max_i:i+1].min()
    if flag_height > pole_height * 0.5: # Flag should smaller vertically than preceding trend
        return False

    pips_x, pips_y = find_pips(data[max_i:i+1], 5, 3) # Finds pips between max and current index (inclusive)

    # Check center pip is greater than two adjacent. \/\/  
    if not (pips_y[2] > pips_y[1] and pips_y[2] > pips_y[3]):
        return False
        
    # Find slope and intercept of flag lines
    # intercept is at the max value (top of pole)
    resist_rise = pips_y[2] - pips_y[0]
    resist_run = pips_x[2] - pips_x[0]
    resist_slope = resist_rise / resist_run
    resist_intercept = pips_y[0] 

    support_rise = pips_y[3] - pips_y[1]
    support_run = pips_x[3] - pips_x[1]
    support_slope = support_rise / support_run
    support_intercept = pips_y[1] + (pips_x[0] - pips_x[1]) * support_slope

    # Find x where two lines intersect.
    if resist_slope != support_slope: # Not parallel
        intersection = (support_intercept - resist_intercept) / (resist_slope - support_slope)
    else:
        intersection = -flag_width * 100

    # No intersection in flag area
    if intersection <= pips_x[4] and intersection >= 0:
        return False
    
    # Filter harshly diverging lines
    if intersection < 0 and intersection > -1.0 * flag_width:
        return False

    # Check if current point has a breakout of flag. (confirmation)
    resist_endpoint = pips_y[0] + resist_slope * pips_x[4]
    if pips_y[4] < resist_endpoint:
        return False

    # Pattern is confiremd, fill out pattern details in pending
    if support_slope > 0:
        pending.pennant = True
    else:
        pending.pennant = False

    pending.tip_x = max_i
    pending.tip_y = data[max_i]
    pending.conf_x = i
    pending.conf_y = data[i]
    pending.flag_width = flag_width
    pending.flag_height = flag_height
    pending.pole_width = pole_width
    pending.pole_height = pole_height
    
    pending.support_slope = support_slope
    pending.support_intercept = support_intercept
    pending.resist_slope = resist_slope
    pending.resist_intercept = resist_intercept
    
    return True

def find_flags_pennants_pips(data: np.array, order:int):
    assert(order >= 3)
    pending_bull = None # Pending pattern
    pending_bear = None # Pending pattern

    bull_pennants = []
    bear_pennants = []
    bull_flags = []
    bear_flags = []
    for i in range(len(data)):

        # Pattern data is organized like so:
        if rw_top(data, i, order):
            pending_bear = FlagPattern(i - order, data[i - order])
        
        if rw_bottom(data, i, order):
            pending_bull = FlagPattern(i - order, data[i - order])

        if pending_bear is not None:
            if check_bear_pattern_pips(pending_bear, data, i, order):
                if pending_bear.pennant:
                    bear_pennants.append(pending_bear)
                else:
                    bear_flags.append(pending_bear)
                pending_bear = None

        if pending_bull is not None:
            if check_bull_pattern_pips(pending_bull, data, i, order):
                if pending_bull.pennant:
                    bull_pennants.append(pending_bull)
                else:
                    bull_flags.append(pending_bull)
                pending_bull = None

    return bull_flags, bear_flags, bull_pennants, bear_pennants

def find_flags_pennants_pips_df(df: pd.DataFrame, order: int = 20) -> Dict[str, List[Dict]]:
    """
    Versão melhorada com filtros adicionais
    """
    patterns = []
    close_prices = df['close'].values
    min_pole_height = df['close'].mean() * 0.02  # 2% do preço médio
    
    bull_flags, bear_flags, bull_pennants, bear_pennants = find_flags_pennants_pips(close_prices, order)
    
    for pattern in bull_flags + bear_flags + bull_pennants + bear_pennants:
        # Filtros adicionais
        if not (pattern.pole_height > min_pole_height and 
                pattern.pole_width >= 5 and
                is_valid_proportion(pattern.pole_height, pattern.flag_height, 
                                   pattern.pole_width, pattern.flag_width)):
            continue
            
        time_start = int(df.index[pattern.tip_x].timestamp())
        time_end = int(df.index[pattern.conf_x].timestamp())
        
        # Determinar o tipo
        if pattern in bull_flags:
            p_type = "bull_flag"
        elif pattern in bear_flags:
            p_type = "bear_flag"
        elif pattern in bull_pennants:
            p_type = "bull_pennant"
        else:
            p_type = "bear_pennant"
        
        # Linha superior
        patterns.append({
            "points": [
                time_start, float(pattern.resist_intercept),
                time_end, float(pattern.resist_intercept + pattern.resist_slope * pattern.flag_width)
            ],
            "type": p_type
        })
        
        # Linha inferior
        patterns.append({
            "points": [
                time_start, float(pattern.support_intercept),
                time_end, float(pattern.support_intercept + pattern.support_slope * pattern.flag_width)
            ],
            "type": p_type
        })

    return patterns

# Trending
def check_bull_pattern_trendline(pending: FlagPattern, data: np.array, i:int, order:int):
    
    # Check if data max less than pole tip 
    if data[pending.tip_x + 1 : i].max() > pending.tip_y:
        return False

    flag_min = data[pending.tip_x:i].min()

    # Find flag/pole height and width
    pole_height = pending.tip_y - pending.base_y
    pole_width = pending.tip_x - pending.base_x
    
    flag_height = pending.tip_y - flag_min
    flag_width = i - pending.tip_x

    if flag_width > pole_width * 0.5: # Flag should be less than half the width of pole
        return False

    if flag_height > pole_height * 0.75: # Flag should smaller vertically than preceding trend
        return False

    # Find trendlines going from flag tip to the previous bar (not including current bar)
    support_coefs, resist_coefs = fit_trendlines_single(data[pending.tip_x:i])
    support_slope, support_intercept = support_coefs[0], support_coefs[1]
    resist_slope, resist_intercept = resist_coefs[0], resist_coefs[1]

    # Check for breakout of upper trendline to confirm pattern
    current_resist = resist_intercept + resist_slope * (flag_width + 1)
    if data[i] <= current_resist:
        return False

    # Pattern is confiremd, fill out pattern details in pending
    if support_slope > 0:
        pending.pennant = True
    else:
        pending.pennant = False

    pending.conf_x = i
    pending.conf_y = data[i]
    pending.flag_width = flag_width
    pending.flag_height = flag_height
    pending.pole_width = pole_width
    pending.pole_height = pole_height
    
    pending.support_slope = support_slope
    pending.support_intercept = support_intercept
    pending.resist_slope = resist_slope
    pending.resist_intercept = resist_intercept

    return True

def check_bear_pattern_trendline(pending: FlagPattern, data: np.array, i:int, order:int):
    # Check if data max less than pole tip 
    if data[pending.tip_x + 1 : i].min() < pending.tip_y:
        return False

    flag_max = data[pending.tip_x:i].max()

    # Find flag/pole height and width
    pole_height = pending.base_y - pending.tip_y
    pole_width = pending.tip_x - pending.base_x
    
    flag_height = flag_max - pending.tip_y
    flag_width = i - pending.tip_x

    if flag_width > pole_width * 0.5: # Flag should be less than half the width of pole
        return False

    if flag_height > pole_height * 0.75: # Flag should smaller vertically than preceding trend
        return False

    # Find trendlines going from flag tip to the previous bar (not including current bar)
    support_coefs, resist_coefs = fit_trendlines_single(data[pending.tip_x:i])
    support_slope, support_intercept = support_coefs[0], support_coefs[1]
    resist_slope, resist_intercept = resist_coefs[0], resist_coefs[1]

    # Check for breakout of lower trendline to confirm pattern
    current_support = support_intercept + support_slope * (flag_width + 1)
    if data[i] >= current_support:
        return False

    # Pattern is confiremd, fill out pattern details in pending
    if resist_slope < 0:
        pending.pennant = True
    else:
        pending.pennant = False

    pending.conf_x = i
    pending.conf_y = data[i]
    pending.flag_width = flag_width
    pending.flag_height = flag_height
    pending.pole_width = pole_width
    pending.pole_height = pole_height
    
    pending.support_slope = support_slope
    pending.support_intercept = support_intercept
    pending.resist_slope = resist_slope
    pending.resist_intercept = resist_intercept

    return True

def find_flags_pennants_trendline(data: np.array, order:int):
    assert(order >= 3)
    pending_bull = None # Pending pattern
    pending_bear = None  # Pending pattern

    last_bottom = -1
    last_top = -1

    bull_pennants = []
    bear_pennants = []
    bull_flags = []
    bear_flags = []
    for i in range(len(data)):

        # Pattern data is organized like so:
        if rw_top(data, i, order):
            last_top = i - order
            if last_bottom != -1:
                pending = FlagPattern(last_bottom, data[last_bottom])
                pending.tip_x = last_top
                pending.tip_y = data[last_top]
                pending_bull = pending
        
        if rw_bottom(data, i, order):
            last_bottom = i - order
            if last_top != -1:
                pending = FlagPattern(last_top, data[last_top])
                pending.tip_x = last_bottom
                pending.tip_y = data[last_bottom]
                pending_bear = pending

        if pending_bear is not None:
            if check_bear_pattern_trendline(pending_bear, data, i, order):
                if pending_bear.pennant:
                    bear_pennants.append(pending_bear)
                else:
                    bear_flags.append(pending_bear)
                pending_bear = None
        
        if pending_bull is not None:
            if check_bull_pattern_trendline(pending_bull, data, i, order):
                if pending_bull.pennant:
                    bull_pennants.append(pending_bull)
                else:
                    bull_flags.append(pending_bull)
                pending_bull = None

    return bull_flags, bear_flags, bull_pennants, bear_pennants

def find_flags_pennants_trendline_df(df: pd.DataFrame, order: int = 20) -> Dict[str, List[Dict]]:
    """
    Detecta padrões de bandeiras/pennants baseados em linhas de tendência e retorna no formato:
    {
        "flag": [
            {
                "points": [time1, price1, time2, price2],  # timestamps em milissegundos
                "type": "bull_flag" | "bear_flag" | "bull_pennant" | "bear_pennant"
            },
            ...
        ]
    }
    """
    patterns = []
    close_prices = df['close'].values
    
    # Encontra padrões usando a função existente
    bull_flags, bear_flags, bull_pennants, bear_pennants = find_flags_pennants_trendline(close_prices, order)
    
    # Processa todos os tipos de padrões
    for pattern_list, pattern_type in [
        (bull_flags, "bull_flag"),
        (bear_flags, "bear_flag"),
        (bull_pennants, "bull_pennant"),
        (bear_pennants, "bear_pennant")
    ]:
        for pattern in pattern_list:
            time_start = int(df.index[pattern.tip_x].timestamp())
            time_end = int(df.index[pattern.conf_x].timestamp())
            
            # Linha superior/resistência
            patterns.append({
                "points": [
                    time_start, float(pattern.resist_intercept),
                    time_end, float(pattern.resist_intercept + pattern.resist_slope * pattern.flag_width)
                ],
                "type": pattern_type
            })
            
            # Linha inferior/suporte
            patterns.append({
                "points": [
                    time_start, float(pattern.support_intercept),
                    time_end, float(pattern.support_intercept + pattern.support_slope * pattern.flag_width)
                ],
                "type": pattern_type
            })

    return patterns

# Signals
def detect_flag_signals(df: pd.DataFrame):
    """
    Adiciona colunas 'flag_buy' e 'flag_sell' ao DataFrame com base no rompimento das bandeiras (flags/pennants).
    """
    df = df.copy()
    df['flags_buy'] = False
    df['flags_sell'] = False

    flags = find_flags_pennants_trendline_df(df)

    for flag in flags:
        points = flag['points']
        direction = flag['type']
        
        # Converte os timestamps para índices no DataFrame
        try:
            dt_start = pd.to_datetime(points[0], unit='s')
            dt_end = pd.to_datetime(points[2], unit='s')

            idx_start = df.index.get_indexer([dt_start], method='nearest')[0]
            idx_end = df.index.get_indexer([dt_end], method='nearest')[0]
        except KeyError:
            continue  # pula se não conseguir localizar os pontos no índice

        if idx_end + 2 >= len(df):
            continue  # evita extrapolar o DataFrame

        # Candle após o fim do padrão (rompimento)
        breakout_idx = idx_end
        breakout_close = df['close'].iloc[breakout_idx]
        previous_close = df['close'].iloc[breakout_idx - 1]

        if "bull" in direction:
            if breakout_close > previous_close:
                df.loc[df.index[breakout_idx], 'flags_buy'] = True
        elif "bear" in direction:
            if breakout_close < previous_close:
                df.loc[df.index[breakout_idx], 'flags_sell'] = True

    return df

# Helpers
def plot_flag(candle_data: pd.DataFrame, pattern: FlagPattern, pad=2):
    if pad < 0:
        pad = 0

    start_i = pattern.base_x - pad
    end_i = pattern.conf_x + 1 + pad
    dat = candle_data.iloc[start_i:end_i]
    idx = dat.index
    
    fig = plt.gcf()
    ax = fig.gca()

    tip_idx = idx[pattern.tip_x - start_i]
    conf_idx = idx[pattern.conf_x - start_i]

    pole_line = [(idx[pattern.base_x - start_i], pattern.base_y), (tip_idx, pattern.tip_y)]
    upper_line = [(tip_idx, pattern.resist_intercept), (conf_idx, pattern.resist_intercept + pattern.resist_slope * pattern.flag_width)]
    lower_line = [(tip_idx, pattern.support_intercept), (conf_idx, pattern.support_intercept + pattern.support_slope * pattern.flag_width)]

    mpf.plot(dat, alines=dict(alines=[pole_line, upper_line, lower_line], colors=['w', 'b', 'b']), type='candle', style='charles', ax=ax)
    plt.show()

def is_valid_proportion(pole_height, flag_height, pole_width, flag_width):
    return (flag_height < pole_height * 0.6 and  # Bandeira deve ser menor que 60% do mastro
            flag_width < pole_width * 0.8)       # Largura da bandeira < 80% do mastro
