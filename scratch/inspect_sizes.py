import os
import pandas as pd

downloads_dir = "C:\\Users\\DUYEN\\Downloads"
files = [
    "chi-tiet-chia-qua-canh_11062026.xlsx",
    "chi-tiet-chia-qua-canh_11062026 (1).xlsx",
    "transfer_11062026-161748.xlsx"
]

print("=== Downloads folder size check ===")
for f in files:
    full_path = os.path.join(downloads_dir, f)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"File: {f} | Size: {size} bytes ({size/1024/1024:.2f} MB)")
        try:
            df = pd.read_excel(full_path, nrows=5)
            # Find row count
            df_full = pd.read_excel(full_path)
            print(f"  Rows count: {len(df_full)}")
        except Exception as e:
            print(f"  Error reading: {e}")
    else:
        print(f"File not found: {f}")
