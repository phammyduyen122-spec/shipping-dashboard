import pandas as pd
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob("transfer_*.xlsx")):
    if "2026-06-08" not in f and "2026-06-09" not in f:
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
        
        # Check from KFM to KHO RAU CỦ or KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG
        df_rev = df[df[from_col].astype(str).str.upper().str.startswith('KFM') & 
                    df[to_col].astype(str).str.strip().isin(['KHO RAU CỦ', 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'])]
        
        print(f"Total rows from ST to KRC or KRCXLCLCH: {len(df_rev)}")
        if len(df_rev) > 0:
            print("Sample rows:")
            print(df_rev[[from_col, to_col, 'Mã chuyển hàng', 'Số lượng chuyển', 'Số lượng nhận']].head(5))
            
    except Exception as e:
        print(f"Error: {e}")
