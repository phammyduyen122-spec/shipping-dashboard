import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_file(filepath):
    print(f"\n--- Checking {filepath} ---")
    try:
        df_raw = pd.read_excel(filepath, header=None, nrows=10)
        header_row = None
        for idx in range(len(df_raw)):
            row_vals = [str(x).lower() for x in df_raw.iloc[idx].values]
            if any('mã hàng' in x for x in row_vals) or any('tên hàng' in x for x in row_vals):
                header_row = idx
                break
        if header_row is None:
            header_row = 0
            
        df = pd.read_excel(filepath, header=header_row)
        
        name_col = None
        for col in df.columns:
            if 'tên hàng' in str(col).lower() or 'tên sản phẩm' in str(col).lower():
                name_col = col
                break
                
        if name_col is None:
            print("No item name column found")
            return
            
        matches = df[df[name_col].fillna("").astype(str).str.lower().str.contains("mận|man")]
        print(f"Found {len(matches)} matches")
        if len(matches) > 0:
            for idx, row in matches.iterrows():
                print(f"Row {idx}:")
                for col in df.columns:
                    print(f"  {col}: {row[col]}")
    except Exception as e:
        print(f"Error: {e}")

check_file("transfer_2026-06-07.xlsx")
check_file("transfer_2026-06-06.xlsx")
