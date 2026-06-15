import pandas as pd
import os
import sys

perf_file = "performance dashboard/chi-tiet-chia-qua-canh_11062026.xlsx"
transfer_file = "transfer_11062026-161748.xlsx"

def safe_print(text):
    sys.stdout.reconfigure(encoding='utf-8')
    print(text.encode('utf-8', errors='replace').decode('utf-8'))

safe_print("=== CHECKING UNIQUE DATES ===")

if os.path.exists(perf_file):
    df_p = pd.read_excel(perf_file)
    safe_print(f"Performance unique dates: {df_p['Ngày chuyển mong muốn'].dropna().unique()[:15]}")
    safe_print(f"Performance row count: {len(df_p)}")
else:
    safe_print(f"File not found: {perf_file}")

if os.path.exists(transfer_file):
    # Find header row
    df_raw = pd.read_excel(transfer_file, header=None, nrows=10)
    header_row = 0
    for idx in range(len(df_raw)):
        row_vals = [str(x).lower() for x in df_raw.iloc[idx].values]
        if any('mã hàng' in x for x in row_vals) or any('tên hàng' in x for x in row_vals):
            header_row = idx
            break
    df_t = pd.read_excel(transfer_file, header=header_row)
    safe_print(f"Transfers unique dates: {df_t['Ngày chuyển hàng'].dropna().unique()[:15]}")
    safe_print(f"Transfers row count: {len(df_t)}")
else:
    safe_print(f"File not found: {transfer_file}")
