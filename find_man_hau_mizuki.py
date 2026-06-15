import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_files = glob.glob("*.xlsx") + glob.glob("performance dashboard/*.xlsx")
print("Files to scan:", excel_files)

for f in excel_files:
    if not os.path.exists(f):
        continue
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
        
        # Normalize columns
        df.columns = [str(c).strip() for c in df.columns]
        
        # Search for columns
        name_col = None
        branch_col = None
        for col in df.columns:
            col_l = col.lower()
            if 'tên hàng' in col_l or 'tên sản phẩm' in col_l:
                name_col = col
            if 'chi nhánh nhận' in col_l or 'nơi nhận' in col_l or 'valora' in col_l or 'bch' in col_l:
                branch_col = col
                
        # If branch_col not found, try the 4th column (index 3)
        if branch_col is None and len(df.columns) > 3:
            branch_col = df.columns[3]
            
        if name_col is None:
            continue
            
        # Search
        for idx, row in df.iterrows():
            item_name = str(row[name_col]).lower()
            to_branch = str(row[branch_col]).lower() if branch_col else ""
            if "mận" in item_name and "hậu" in item_name and "mizuki" in to_branch:
                print(f"\nMatch found in {f} at row {idx}:")
                for col in df.columns:
                    print(f"  {col}: {row[col]}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
