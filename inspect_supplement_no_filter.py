import pandas as pd
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob("transfer_*.xlsx")):
    if "2026-06-07" not in f and "2026-06-08" not in f and "2026-06-09" not in f:
        continue
    print(f"\n--- File: {f} ---")
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
        shipped_col = [c for c in df.columns if 'chuyển' in c.lower() and 'lượng' in c.lower()][0]
        received_col = [c for c in df.columns if 'nhận' in c.lower() and 'lượng' in c.lower()][0]
        status_col = [c for c in df.columns if 'trạng thái' in c.lower()][0]
        
        # Clean numeric
        df[shipped_col] = pd.to_numeric(df[shipped_col], errors='coerce').fillna(0).astype(float)
        df[received_col] = pd.to_numeric(df[received_col], errors='coerce').fillna(0).astype(float)
        
        # Original rows
        df_orig = df[df[from_col].astype(str).str.strip() == 'KHO RAU CỦ']
        df_orig = df_orig[~df_orig[status_col].astype(str).str.lower().str.contains('hủy|huy')]
        
        # Cap original received: received <= shipped (if received != -1)
        orig_shipped = df_orig[shipped_col].sum()
        
        # Capping
        df_orig_capped = df_orig.copy()
        mask = (df_orig_capped[received_col] > df_orig_capped[shipped_col]) & (df_orig_capped[received_col] != -1)
        df_orig_capped.loc[mask, received_col] = df_orig_capped.loc[mask, shipped_col]
        
        # Original received (excluding -1 rows for shortage sum, but let's see how much shortage)
        # Actually shortage = sum(shipped - received) for rows where received != -1
        mask_not_transit = df_orig_capped[received_col] != -1
        orig_shortage = (df_orig_capped.loc[mask_not_transit, shipped_col] - df_orig_capped.loc[mask_not_transit, received_col]).sum()
        
        # Correctives
        df_corr = df[df[from_col].astype(str).str.strip() == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
        df_corr = df_corr[df_corr[to_col].astype(str).str.upper().str.startswith('KFM')]
        df_corr = df_corr[~df_corr[status_col].astype(str).str.lower().str.contains('hủy|huy')]
        
        # Sum of correctives received (excluding -1)
        corr_received_sum = df_corr.loc[df_corr[received_col] != -1, received_col].sum()
        
        print(f"Original Shipped: {orig_shipped:.2f}")
        print(f"Original Shortage: {orig_shortage:.2f}")
        print(f"Correctives from KRCXLCLCH to ST (total rows: {len(df_corr)}):")
        print(f"  Sum of Received (excluding -1): {corr_received_sum:.2f}")
        print(f"  Remaining Shortage: {orig_shortage - corr_received_sum:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
