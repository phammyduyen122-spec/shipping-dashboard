import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f = "transfer_09062026-165346.xlsx"
print(f"Reading {f}...")
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
    
    from_col = [c for c in df.columns if 'chuyển' in c.lower() and 'nhánh' in c.lower() or 'nơi chuyển' in c.lower() or 'chi nhánh chuyển' in c.lower()][0]
    to_col = [c for c in df.columns if 'nhận' in c.lower() and 'nhánh' in c.lower() or 'nơi nhận' in c.lower() or 'chi nhánh nhận' in c.lower()][0]
    code_col = [c for c in df.columns if 'mã hàng' in c.lower() or 'mã hàng' == c.lower() or 'mã' in c.lower() and 'hàng' in c.lower()][0]
    shipped_col = [c for c in df.columns if 'chuyển' in c.lower() and 'lượng' in c.lower()][0]
    received_col = [c for c in df.columns if 'nhận' in c.lower() and 'lượng' in c.lower()][0]
    status_col = [c for c in df.columns if 'trạng thái' in c.lower()][0]
    
    # Clean numeric
    df[shipped_col] = pd.to_numeric(df[shipped_col], errors='coerce').fillna(0).astype(float)
    df[received_col] = pd.to_numeric(df[received_col], errors='coerce').fillna(0).astype(float)
    
    df_sku = df[df[code_col].astype(str).str.strip() == '1101392']
    print(f"Total raw rows for SKU 1101392: {len(df_sku)}")
    
    # Check from KHO RAU CỦ
    df_orig = df_sku[df_sku[from_col].astype(str).str.strip() == 'KHO RAU CỦ']
    print(f"Original rows (from KHO RAU CỦ): {len(df_orig)}")
    
    shortages = df_orig[df_orig[received_col] < df_orig[shipped_col]]
    print(f"Shortage rows (received < shipped): {len(shortages)}")
    if len(shortages) > 0:
        print("\nAll shortage rows for this SKU:")
        print(shortages[[from_col, to_col, shipped_col, received_col, status_col]])
        
except Exception as e:
    print(f"Error: {e}")
