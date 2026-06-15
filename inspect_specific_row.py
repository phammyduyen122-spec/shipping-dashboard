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
    po_col = [c for c in df.columns if 'mã chuyển hàng' in c.lower() or 'mã chuyển' in c.lower() or 'mã phiếu' in c.lower() or 'phiếu chuyển' in c.lower()][0]
    
    # Let's inspect row 2081 specifically
    r2081 = df.iloc[2081]
    po_code = r2081[po_col]
    item_code = r2081[code_col]
    store = r2081[to_col]
    
    print(f"\nRow 2081 info:")
    print(f"  PO Code: {po_code} | SKU: {item_code} | Store: {store} | Shipped: {r2081[shipped_col]} | Received: {r2081[received_col]}")
    
    # Find all rows in excel with the same PO Code, SKU, and Store
    duplicates = df[(df[po_col] == po_code) & (df[code_col] == item_code) & (df[to_col] == store)]
    print(f"\nAll rows with PO={po_code}, SKU={item_code}, Store={store}:")
    print(duplicates[[po_col, from_col, to_col, code_col, shipped_col, received_col, status_col]])
    
except Exception as e:
    print(f"Error: {e}")
