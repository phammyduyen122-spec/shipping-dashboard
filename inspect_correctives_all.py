import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob("transfer_*.xlsx")):
    if "2026-06-08" not in f and "2026-06-09" not in f:
        continue
    print(f"\n--- File: {f} ---")
    try:
        # Load header
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
        
        # Lower case columns
        df.columns = [str(c).strip() for c in df.columns]
        
        from_col = [c for c in df.columns if 'chuyển' in c.lower() and 'nhánh' in c.lower() or 'nơi chuyển' in c.lower() or 'chi nhánh chuyển' in c.lower()][0]
        to_col = [c for c in df.columns if 'nhận' in c.lower() and 'nhánh' in c.lower() or 'nơi nhận' in c.lower() or 'chi nhánh nhận' in c.lower()][0]
        code_col = [c for c in df.columns if 'mã' in c.lower() and 'chuyển' in c.lower()][0]
        orig_col = [c for c in df.columns if 'gốc' in c.lower() or 'chứng từ gốc' in c.lower()][0]
        shipped_col = [c for c in df.columns if 'chuyển' in c.lower() and 'lượng' in c.lower()][0]
        received_col = [c for c in df.columns if 'nhận' in c.lower() and 'lượng' in c.lower()][0]
        
        print(f"Columns mapping: From='{from_col}', To='{to_col}', Code='{code_col}', Orig='{orig_col}'")
        
        df_corr = df[df[from_col].astype(str).str.strip() == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
        print(f"Total corrective rows: {len(df_corr)}")
        
        # Categorize
        kfm_dest = df_corr[df_corr[to_col].astype(str).str.upper().str.startswith('KFM')]
        non_kfm_dest = df_corr[~df_corr[to_col].astype(str).str.upper().str.startswith('KFM')]
        
        print(f"  To Supermarkets (KFM): {len(kfm_dest)}")
        print(f"  To Warehouses/Others: {len(non_kfm_dest)}")
        
        human = kfm_dest[kfm_dest[orig_col].fillna("").astype(str).str.strip() == ""]
        auto = kfm_dest[kfm_dest[orig_col].fillna("").astype(str).str.strip() != ""]
        
        print(f"    Human-created (empty orig): {len(human)}")
        print(f"    Auto-created (non-empty orig): {len(auto)}")
        
        if len(auto) > 0:
            print("    Sample Auto originalDoc values:")
            print(auto[[code_col, to_col, orig_col, shipped_col, received_col]].head(10))
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
