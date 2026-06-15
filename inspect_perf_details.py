import openpyxl
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard/chi-tiet-chia-qua-canh_04062026 (3).xlsx"

df = pd.read_excel(file_path, sheet_name="Sheet 1")
print(f"Total rows: {len(df)}")
print("--- Unique values count for key columns ---")
for col in ['Trạng thái', 'Trạng thái nhận hàng (PR)', 'Trạng thái chuyển hàng', 'Nơi chuyển', 'Nơi nhận', 'Người chia hàng']:
    if col in df.columns:
        print(f"\n{col}: {df[col].nunique()} unique values")
        print(df[col].value_counts().head(5))

print("\n--- Column types and null counts ---")
print(df.info())
