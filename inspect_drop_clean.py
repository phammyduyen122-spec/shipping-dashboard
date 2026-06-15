import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

perf_dir = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
perf_files = glob.glob(os.path.join(perf_dir, "*.xlsx"))
perf_file = max(perf_files, key=os.path.getmtime)
df = pd.read_excel(perf_file, sheet_name="Sheet 1")

print("Original size:", len(df))
print("Unique states in original:")
print(df['Trạng thái'].value_counts(dropna=False))

df_no_cancelled = df[~df['Trạng thái'].str.lower().str.contains('hủy|huy', na=False)]
print("After removing cancel:", len(df_no_cancelled))
print("Unique states in df_no_cancelled:")
print(df_no_cancelled['Trạng thái'].value_counts(dropna=False))

df_no_cc = df_no_cancelled[~df_no_cancelled['Barcode'].astype(str).isin(['CC00360', 'CC00381'])]
print("After removing CC00360/CC00381:", len(df_no_cc))
print("Unique states in df_no_cc:")
print(df_no_cc['Trạng thái'].value_counts(dropna=False))

print("Is there any nan itemCode filter or something in test_perf_parse.py?")
# Let's check test_perf_parse.py again:
# Wait, did we do `df_clean = df_clean[df_clean['barcode'] != 'nan']` or similar? No.
# Wait, why was Clean rows 1014 in test_perf_parse.py? Let's check its filter code again.
# Ah, in test_perf_parse.py:
# `df_clean = df_clean[~df_clean['trangThai'].str.lower().str.contains('hủy|huy', na=False)]`
# Wait! Let's check if there is any other column that had NaNs or if some filter was active.
