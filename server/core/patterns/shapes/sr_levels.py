import pandas as pd
import numpy as np
from typing import Tuple, List

def pivotid(df, l, n1, n2):
    """
    Identifies pivot points (high, low, or both) in a DataFrame.
    """
    l = int(l)
    n1 = int(n1)
    n2 = int(n2)

    if l - n1 < 0 or l + n2 >= len(df):
        return 0

    pividlow = 1
    pividhigh = 1
    
    # Check for pivot low
    for i in range(l - n1, l + n2 + 1):
        if df.iloc[l]['low'] > df.iloc[i]['low']:
            pividlow = 0
            break
            
    # Check for pivot high
    for i in range(l - n1, l + n2 + 1):
        if df.iloc[l]['high'] < df.iloc[i]['high']:
            pividhigh = 0
            break
            
    if pividlow and pividhigh:
        return 3
    elif pividlow:
        return 1
    elif pividhigh:
        return 2
    else:
        return 0

def calculate_atr(df, period=14):
    """
    Calcula o Average True Range para determinar tolerâncias dinâmicas.
    """
    df_temp = df.copy()
    df_temp['h_l'] = df_temp['high'] - df_temp['low']
    df_temp['h_c'] = abs(df_temp['high'] - df_temp['close'].shift(1))
    df_temp['l_c'] = abs(df_temp['low'] - df_temp['close'].shift(1))
    
    df_temp['tr'] = df_temp[['h_l', 'h_c', 'l_c']].max(axis=1)
    atr = df_temp['tr'].rolling(window=period).mean()
    
    return atr

def calculate_volume_profile(df, lookback=50):
    """
    Calcula perfil de volume simples para identificar níveis mais significativos.
    """
    volume_at_price = {}
    
    for i in range(max(0, len(df) - lookback), len(df)):
        price_level = round((df.iloc[i]['high'] + df.iloc[i]['low']) / 2, 2)
        volume = df.iloc[i].get('volume', 1)  # Default volume = 1 se não existir
        
        if price_level in volume_at_price:
            volume_at_price[price_level] += volume
        else:
            volume_at_price[price_level] = volume
    
    return volume_at_price

def filter_significant_levels(levels, current_price, min_distance_pct=0.5, max_levels=10):
    """
    Filtra níveis mais significativos baseado na distância do preço atual.
    """
    if not levels:
        return []
    
    # Calcula distância percentual de cada nível
    level_distances = [(level, abs(level - current_price) / current_price * 100) for level in levels]
    
    # Filtra níveis muito próximos entre si
    filtered_levels = []
    sorted_levels = sorted(level_distances, key=lambda x: x[1])  # Ordena por distância
    
    for level, distance in sorted_levels:
        # Verifica se há algum nível muito próximo já adicionado
        too_close = any(abs(level - existing) / existing * 100 < min_distance_pct 
                       for existing in filtered_levels)
        
        if not too_close and len(filtered_levels) < max_levels:
            filtered_levels.append(level)
    
    return sorted(filtered_levels)

def calculate_momentum_confirmation(df, index, lookback=5):
    """
    Calcula confirmação de momentum usando RSI simples e mudança de preço.
    """
    if index < lookback:
        return 0
    
    # RSI simples
    price_changes = []
    for i in range(index - lookback + 1, index + 1):
        if i > 0:
            change = df.iloc[i]['close'] - df.iloc[i-1]['close']
            price_changes.append(change)
    
    if not price_changes:
        return 0
    
    gains = [change for change in price_changes if change > 0]
    losses = [-change for change in price_changes if change < 0]
    
    avg_gain = sum(gains) / len(gains) if gains else 0.01
    avg_loss = sum(losses) / len(losses) if losses else 0.01
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def detect_support_resistance_signals(df, n1=5, n2=5, min_touches=2, volume_factor=0.005):
    """
    Versão melhorada para detectar sinais de suporte e resistência com maior acurácia.
    
    Args:
        df: DataFrame com dados OHLCV
        n1, n2: Parâmetros para detecção de pivots
        min_touches: Número mínimo de toques para confirmar nível
        volume_factor: Fator para confirmar breakouts com volume
    """
    df_copy = df.copy()
    
    # Calcula ATR para tolerâncias dinâmicas
    atr = calculate_atr(df_copy)
    df_copy['atr'] = atr
    
    # Detecta pivots
    pivot_values = [0] * len(df_copy)
    for l_idx in range(len(df_copy)):
        pivot_values[l_idx] = pivotid(df_copy, l_idx, n1, n2)
    
    df_copy['pivot'] = pivot_values
    
    # Coleta níveis de suporte e resistência com informações adicionais
    support_data = []
    resistance_data = []
    
    for i in range(len(df_copy)):
        if df_copy.iloc[i]['pivot'] == 1:  # Support
            support_data.append({
                'price': df_copy.iloc[i]['low'],
                'index': i,
                'volume': df_copy.iloc[i].get('volume', 1)
            })
        elif df_copy.iloc[i]['pivot'] == 2:  # Resistance
            resistance_data.append({
                'price': df_copy.iloc[i]['high'],
                'index': i,
                'volume': df_copy.iloc[i].get('volume', 1)
            })
    
    # Agrupa níveis próximos e conta toques
    def group_and_count_touches(level_data, tolerance_pct=0.3):
        if not level_data:
            return []
        
        grouped_levels = []
        sorted_data = sorted(level_data, key=lambda x: x['price'])
        
        current_group = [sorted_data[0]]
        
        for data in sorted_data[1:]:
            # Se o nível está próximo do grupo atual
            avg_price = sum(d['price'] for d in current_group) / len(current_group)
            if abs(data['price'] - avg_price) / avg_price * 100 < tolerance_pct:
                current_group.append(data)
            else:
                # Finaliza grupo atual
                if len(current_group) >= min_touches:
                    group_price = sum(d['price'] for d in current_group) / len(current_group)
                    group_volume = sum(d['volume'] for d in current_group)
                    grouped_levels.append({
                        'price': group_price,
                        'touches': len(current_group),
                        'volume': group_volume,
                        'strength': len(current_group) * group_volume
                    })
                current_group = [data]
        
        # Adiciona último grupo
        if len(current_group) >= min_touches:
            group_price = sum(d['price'] for d in current_group) / len(current_group)
            group_volume = sum(d['volume'] for d in current_group)
            grouped_levels.append({
                'price': group_price,
                'touches': len(current_group),
                'volume': group_volume,
                'strength': len(current_group) * group_volume
            })
        
        return grouped_levels
    
    # Agrupa e filtra níveis significativos
    significant_supports = group_and_count_touches(support_data)
    significant_resistances = group_and_count_touches(resistance_data)
    
    # Ordena por força (toques * volume)
    significant_supports.sort(key=lambda x: x['strength'], reverse=True)
    significant_resistances.sort(key=lambda x: x['strength'], reverse=True)
    
    # Mantém apenas os níveis mais fortes
    significant_supports = significant_supports[:8]
    significant_resistances = significant_resistances[:8]
    
    # Inicializa colunas de sinal
    df_copy['sr_buy'] = False
    df_copy['sr_sell'] = False
    df_copy['signal_strength'] = 0.0
    df_copy['signal_type'] = ''
    
    # Gera sinais com múltiplas confirmações
    for i in range(max(20, n1), len(df_copy)):
        current_close = df_copy.iloc[i]['close']
        current_open = df_copy.iloc[i]['open']
        current_high = df_copy.iloc[i]['high']
        current_low = df_copy.iloc[i]['low']
        current_volume = df_copy.iloc[i].get('volume', 1)
        current_atr = df_copy.iloc[i]['atr'] if not pd.isna(df_copy.iloc[i]['atr']) else 0.01
        
        # Volume médio para comparação
        avg_volume = df_copy['volume'].iloc[max(0, i-20):i].mean() if 'volume' in df_copy.columns else 1
        
        # Momentum
        rsi = calculate_momentum_confirmation(df_copy, i)
        
        # SINAIS DE COMPRA
        for support in significant_supports:
            support_price = support['price']
            support_strength = support['touches']
            tolerance = current_atr * 0.5
            
            # Condições para sinal de compra
            conditions_buy = []
            
            # 1. Preço próximo ao suporte
            price_near_support = abs(current_low - support_price) <= tolerance
            conditions_buy.append(price_near_support)
            
            # 2. Candle bullish (fechamento > abertura)
            bullish_candle = current_close > current_open
            conditions_buy.append(bullish_candle)
            
            # 3. RSI não está em sobrecompra (< 70)
            rsi_ok = rsi < 70
            conditions_buy.append(rsi_ok)
            
            # 4. Volume acima da média (confirmação)
            volume_confirmation = current_volume > avg_volume * 1.2
            conditions_buy.append(volume_confirmation)
            
            # 5. Preço não quebrou o suporte significativamente
            no_breakdown = current_close > support_price - tolerance
            conditions_buy.append(no_breakdown)
            
            # 6. Trend de curto prazo (últimas 3 velas não são todas bearish)
            recent_closes = [df_copy.iloc[j]['close'] for j in range(max(0, i-2), i+1)]
            recent_opens = [df_copy.iloc[j]['open'] for j in range(max(0, i-2), i+1)]
            bearish_streak = sum(1 for c, o in zip(recent_closes, recent_opens) if c < o)
            trend_ok = bearish_streak < 3
            conditions_buy.append(trend_ok)
            
            # Calcula força do sinal
            conditions_met = sum(conditions_buy)
            signal_strength = (conditions_met / len(conditions_buy)) * support_strength
            
            # Gera sinal se pelo menos 5 de 6 condições forem atendidas
            if conditions_met >= 5 and signal_strength > df_copy.iloc[i]['signal_strength']:
                df_copy.loc[df_copy.index[i], 'sr_buy'] = True
                df_copy.loc[df_copy.index[i], 'signal_strength'] = signal_strength
                df_copy.loc[df_copy.index[i], 'signal_type'] = f'Support_Bounce_{support_strength}touches'
        
        # SINAIS DE VENDA
        for resistance in significant_resistances:
            resistance_price = resistance['price']
            resistance_strength = resistance['touches']
            tolerance = current_atr * 0.5
            
            conditions_sell = []
            
            # 1. Preço próximo à resistência
            price_near_resistance = abs(current_high - resistance_price) <= tolerance
            conditions_sell.append(price_near_resistance)
            
            # 2. Candle bearish
            bearish_candle = current_close < current_open
            conditions_sell.append(bearish_candle)
            
            # 3. RSI não está em sobrevenda (> 30)
            rsi_ok = rsi > 30
            conditions_sell.append(rsi_ok)
            
            # 4. Volume acima da média
            volume_confirmation = current_volume > avg_volume * 1.2
            conditions_sell.append(volume_confirmation)
            
            # 5. Preço não quebrou a resistência significativamente
            no_breakout = current_close < resistance_price + tolerance
            conditions_sell.append(no_breakout)
            
            # 6. Trend de curto prazo (últimas 3 velas não são todas bullish)
            recent_closes = [df_copy.iloc[j]['close'] for j in range(max(0, i-2), i+1)]
            recent_opens = [df_copy.iloc[j]['open'] for j in range(max(0, i-2), i+1)]
            bullish_streak = sum(1 for c, o in zip(recent_closes, recent_opens) if c > o)
            trend_ok = bullish_streak < 3
            conditions_sell.append(trend_ok)
            
            conditions_met = sum(conditions_sell)
            signal_strength = (conditions_met / len(conditions_sell)) * resistance_strength
            
            if conditions_met >= 5 and signal_strength > abs(df_copy.iloc[i]['signal_strength']):
                df_copy.loc[df_copy.index[i], 'sr_sell'] = True
                df_copy.loc[df_copy.index[i], 'signal_strength'] = -signal_strength
                df_copy.loc[df_copy.index[i], 'signal_type'] = f'Resistance_Rejection_{resistance_strength}touches'
    
    # Armazena níveis detectados
    support_levels = [s['price'] for s in significant_supports]
    resistance_levels = [r['price'] for r in significant_resistances]
    
    df_copy['support_levels_detected'] = [support_levels] * len(df_copy)
    df_copy['resistance_levels_detected'] = [resistance_levels] * len(df_copy)
    
    return df_copy

def get_support_resistance_levels(df, n1=5, n2=5, min_touches=2):
    """
    Versão melhorada para extrair apenas os níveis de suporte e resistência.
    """
    # Detecta pivots
    support_data = []
    resistance_data = []
    
    for l_idx in range(len(df)):
        pivot_type = pivotid(df, l_idx, n1, n2)
        if pivot_type == 1:  # Support
            support_data.append({
                'price': df.iloc[l_idx]['low'],
                'volume': df.iloc[l_idx].get('volume', 1)
            })
        elif pivot_type == 2:  # Resistance
            resistance_data.append({
                'price': df.iloc[l_idx]['high'],
                'volume': df.iloc[l_idx].get('volume', 1)
            })
    
    # Agrupa níveis próximos
    def group_levels(level_data, tolerance_pct=0.3):
        if not level_data:
            return []
        
        grouped = []
        sorted_data = sorted(level_data, key=lambda x: x['price'])
        current_group = [sorted_data[0]]
        
        for data in sorted_data[1:]:
            avg_price = sum(d['price'] for d in current_group) / len(current_group)
            if abs(data['price'] - avg_price) / avg_price * 100 < tolerance_pct:
                current_group.append(data)
            else:
                if len(current_group) >= min_touches:
                    group_price = sum(d['price'] for d in current_group) / len(current_group)
                    grouped.append(group_price)
                current_group = [data]
        
        if len(current_group) >= min_touches:
            group_price = sum(d['price'] for d in current_group) / len(current_group)
            grouped.append(group_price)
        
        return grouped
    
    support_levels = group_levels(support_data)
    resistance_levels = group_levels(resistance_data)
    
    return support_levels + resistance_levels

# Função adicional para backtesting dos sinais
def backtest_signals(df_with_signals, stop_loss_atr_mult=1.5, take_profit_atr_mult=3.0):
    """
    Realiza backtest simples dos sinais gerados.
    """
    results = []
    position = None
    
    for i in range(len(df_with_signals)):
        row = df_with_signals.iloc[i]
        current_price = row['close']
        current_atr = row.get('atr', 0.01)
        
        # Fecha posição existente se necessário
        if position:
            if position['type'] == 'long':
                if current_price <= position['stop_loss'] or current_price >= position['take_profit']:
                    pnl = current_price - position['entry_price']
                    results.append({
                        'entry_date': position['entry_date'],
                        'exit_date': row.name if hasattr(row, 'name') else i,
                        'type': 'long',
                        'entry_price': position['entry_price'],
                        'exit_price': current_price,
                        'pnl': pnl,
                        'pnl_pct': pnl / position['entry_price'] * 100,
                        'signal_strength': position['signal_strength']
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current_price >= position['stop_loss'] or current_price <= position['take_profit']:
                    pnl = position['entry_price'] - current_price
                    results.append({
                        'entry_date': position['entry_date'],
                        'exit_date': row.name if hasattr(row, 'name') else i,
                        'type': 'short',
                        'entry_price': position['entry_price'],
                        'exit_price': current_price,
                        'pnl': pnl,
                        'pnl_pct': pnl / position['entry_price'] * 100,
                        'signal_strength': position['signal_strength']
                    })
                    position = None
        
        # Abre nova posição
        if not position:
            if row['sr_buy']:
                position = {
                    'type': 'long',
                    'entry_price': current_price,
                    'entry_date': row.name if hasattr(row, 'name') else i,
                    'stop_loss': current_price - (current_atr * stop_loss_atr_mult),
                    'take_profit': current_price + (current_atr * take_profit_atr_mult),
                    'signal_strength': row.get('signal_strength', 1)
                }
            
            elif row['sr_sell']:
                position = {
                    'type': 'short',
                    'entry_price': current_price,
                    'entry_date': row.name if hasattr(row, 'name') else i,
                    'stop_loss': current_price + (current_atr * stop_loss_atr_mult),
                    'take_profit': current_price - (current_atr * take_profit_atr_mult),
                    'signal_strength': abs(row.get('signal_strength', 1))
                }
    
    if results:
        results_df = pd.DataFrame(results)
        win_rate = len(results_df[results_df['pnl'] > 0]) / len(results_df) * 100
        avg_pnl = results_df['pnl_pct'].mean()
        
        print(f"Backtest Results:")
        print(f"Total Trades: {len(results_df)}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Average PnL: {avg_pnl:.2f}%")
        print(f"Best Trade: {results_df['pnl_pct'].max():.2f}%")
        print(f"Worst Trade: {results_df['pnl_pct'].min():.2f}%")
        
        return results_df
    else:
        print("No trades generated")
        return pd.DataFrame()