import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f = "transfer_09062026-165346.xlsx"
try:
    df_raw = pd.read_excel(f, header=None, nrows=10)
    header_row = None
    for idx in range(len(df_raw)):
        row_vals = [str(x).lower() for x in df_raw.iloc[idx].values]
        if any('mã hàng' in x for x in row_vals) or any('tên hàng' in x for x in row_vals):
            header_row = idx
            break
    if header_row is None:
        header_row = 0
    df = pd.read_excel(f, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]
    
    date_col = [c for c in df.columns if 'ngày' in c.lower()][0]
    
    r2081 = df.iloc[2081]
    print(f"Row 2081 Raw Date: '{r2081[date_col]}' (type: {type(r2081[date_col])})")
    
except Exception as e:
    print(f"Error: {e}")
