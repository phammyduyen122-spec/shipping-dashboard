import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# File 1: transfer
f1 = "transfer_09062026-165346.xlsx"
print(f"Reading {f1}...")
try:
    df1 = pd.read_excel(f1)
    date_cols1 = [c for c in df1.columns if 'ngày' in str(c).lower()]
    if date_cols1:
        col = date_cols1[0]
        print(f"  Date column: {col}")
        print(f"  Total rows: {len(df1)}")
        print(f"  Unique dates in file: {df1[col].unique()}")
    else:
        print("  No date column found!")
except Exception as e:
    print(f"  Error: {e}")

# File 2: performance
f2 = "performance dashboard/chi-tiet-chia-qua-canh_09062026.xlsx"
print(f"\nReading {f2}...")
try:
    df2 = pd.read_excel(f2)
    date_cols2 = [c for c in df2.columns if 'ngày' in str(c).lower()]
    if date_cols2:
        col = date_cols2[0]
        print(f"  Date column: {col}")
        print(f"  Total rows: {len(df2)}")
        print(f"  Unique dates in file: {df2[col].unique()[:15]}")
    else:
        print("  No date column found!")
except Exception as e:
    print(f"  Error: {e}")
