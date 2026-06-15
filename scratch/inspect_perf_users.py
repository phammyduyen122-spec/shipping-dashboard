import pandas as pd
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel("performance dashboard/chi-tiet-chia-qua-canh_09062026.xlsx", sheet_name=0)
col = "Người chia hàng"
if col in df.columns:
    users = df[col].dropna().unique()
    print("Unique users in performance file:")
    for u in sorted(users):
        norm_u = unicodedata.normalize('NFC', str(u))
        print(f"  - '{norm_u}'")
else:
    print(f"Column '{col}' not found in columns: {list(df.columns)}")
