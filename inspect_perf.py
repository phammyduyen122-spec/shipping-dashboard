import openpyxl
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard/chi-tiet-chia-qua-canh_04062026 (3).xlsx"

print("Loading file...")
xls = pd.ExcelFile(file_path)
print("Sheet names:", xls.sheet_names)

for sheet in xls.sheet_names[:3]:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
    print("Columns:", df.columns.tolist())
    print("First 2 rows:")
    print(df.head(2).to_string())
