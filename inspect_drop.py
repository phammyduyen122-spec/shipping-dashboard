import pandas as pd
import glob
import os

perf_dir = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
perf_files = glob.glob(os.path.join(perf_dir, "*.xlsx"))
perf_file = max(perf_files, key=os.path.getmtime)
df = pd.read_excel(perf_file, sheet_name="Sheet 1")

print("Original size:", len(df))
print("Null barcodes:", df['Barcode'].isna().sum())
print("Value counts of Trạng thái in original:")
print(df['Trạng thái'].value_counts(dropna=False))

# Try filtering steps one by one
df_no_cancelled = df[~df['Trạng thái'].str.lower().str.contains('hủy|huy', na=False)]
print("After removing cancel:", len(df_no_cancelled))

df_no_cc = df_no_cancelled[~df_no_cancelled['Barcode'].astype(str).isin(['CC00360', 'CC00381'])]
print("After removing CC00360/CC00381:", len(df_no_cc))

# Wait, check if there was any check like itemCode != 'nan' or itemCode != ''
# Let's see if the code had:
# df_clean = df_clean[df_clean['barcode'] != 'nan']
# wait, did we do anything like that?
# Let's check df_no_cc barcodes
print("Barcodes that are null or nan in df_no_cc:")
print((df_no_cc['Barcode'].astype(str) == 'nan').sum())
print((df_no_cc['Barcode'].astype(str) == '').sum())
