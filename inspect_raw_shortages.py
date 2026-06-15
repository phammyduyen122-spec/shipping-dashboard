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
    shipped_col = [c for c in df.columns if 'chuyển' in c.lower() and 'lượng' in c.lower()][0]
    received_col = [c for c in df.columns if 'nhận' in c.lower() and 'lượng' in c.lower()][0]
    status_col = [c for c in df.columns if 'trạng thái' in c.lower()][0]
    
    # Clean numeric
    df[shipped_col] = pd.to_numeric(df[shipped_col], errors='coerce').fillna(0).astype(float)
    df[received_col] = pd.to_numeric(df[received_col], errors='coerce').fillna(0).astype(float)
    
    df_orig = df[df[from_col].astype(str).str.strip() == 'KHO RAU CỦ']
    df_orig = df_orig[~df_orig[status_col].astype(str).str.lower().str.contains('hủy|huy')]
    
    total_orig = len(df_orig)
    shortage_rows = df_orig[(df_orig[received_col] < df_orig[shipped_col]) & (df_orig[received_col] != -1)]
    surplus_rows = df_orig[(df_orig[received_col] > df_orig[shipped_col]) & (df_orig[received_col] != -1)]
    transit_rows = df_orig[df_orig[received_col] == -1]
    matching_rows = df_orig[df_orig[received_col] == df_orig[shipped_col]]
    
    print(f"Total original rows (KHO RAU CỦ): {total_orig}")
    print(f"  Shortage rows (received < shipped): {len(shortage_rows)}")
    print(f"  Surplus rows (received > shipped): {len(surplus_rows)}")
    print(f"  Transit rows (received == -1): {len(transit_rows)}")
    print(f"  Matching rows (received == shipped): {len(matching_rows)}")
    
    if len(shortage_rows) > 0:
        print("\nSample shortage rows in raw excel:")
        print(shortage_rows[[from_col, shipped_col, received_col, status_col]].head(5))
        
except Exception as e:
    print(f"Error: {e}")
