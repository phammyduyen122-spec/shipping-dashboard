import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Step 1: Globbing files in shipping-dashboard...")
excel_files = glob.glob("transfer_*.xlsx") + glob.glob("*.xlsx")
excel_files = list(set(excel_files))
print("Excel files found:", excel_files)
excel_file = max(excel_files, key=os.path.getmtime)
print("Latest excel file:", excel_file)

print("Step 2: Reading shipping-dashboard excel file...")
df = pd.read_excel(excel_file, header=1)
print("Done. Rows:", len(df))

print("Step 3: Globbing performance dashboard files...")
perf_dir = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
perf_files = glob.glob(os.path.join(perf_dir, "*.xlsx"))
print("Perf files found:", perf_files)
perf_file = max(perf_files, key=os.path.getmtime)
print("Latest perf file:", perf_file)

print("Step 4: Reading performance dashboard excel file...")
df_perf = pd.read_excel(perf_file, sheet_name="Sheet 1")
print("Done. Rows:", len(df_perf))
print("Success!")
