"""Read the one-minute index files and cache them as pickles."""
import os
import pandas as pd

for n in ['VN30', 'VNINDEX']:
    csv = f'data/{n}_1min.csv.gz'
    if os.path.exists(csv):
        df = pd.read_csv(csv, parse_dates=['TradingDate'])
    else:  # original FiinGroup Excel files, if available
        df = pd.read_excel(f'data/{n}.xlsx', engine='openpyxl')
    df.to_pickle(f'data/{n}.pkl')
    print(n, df.shape)
