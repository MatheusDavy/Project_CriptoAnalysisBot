import pandas as pd

from core.patterns.shapes.sr_levels import get_support_resistance_levels
from core.patterns.shapes.flags import find_flags_pennants_trendline_df, find_flags_pennants_pips_df
from core.patterns.shapes.hs import detect_hs_patterns
from core.patterns.shapes.fibonacci import calculate_fibonacci_lines

def generate_shapes(candles, analysis):
    df = pd.DataFrame(candles)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)

    sr = []
    flag = []
    hs = []
    fibonacci = []

    print(analysis['sr'])

    if analysis['sr']:
        sr = get_support_resistance_levels(df)

    if analysis['flags']:
        flag = find_flags_pennants_trendline_df(df)

    if analysis['hs']:
        hs = detect_hs_patterns(df)

    if analysis['fibonacci']:
        fibonacci = calculate_fibonacci_lines(df)

    return {
        "sr": sr,
        "flag": flag,
        "hs": hs,
        "fibonacci": fibonacci
    }
