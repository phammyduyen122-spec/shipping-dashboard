import pandas as pd

f_path = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard/chi-tiet-chia-qua-canh_06062026.xlsx"
df = pd.read_excel(f_path)
df.columns = [str(c).strip() for c in df.columns]

# Filter for dừa
df_dua = df[df['Tên sản phẩm'].str.contains('dừa|dua', case=False, na=False)]
df_combo3 = df_dua[df_dua['Tên sản phẩm'].str.contains('combo 3|3 trái|3 quả', case=False, na=False)]

with open("inspect_perf_dua.txt", "w", encoding="utf-8") as f_out:
    f_out.write(f"Total rows in df: {len(df)}\n")
    f_out.write(f"Total combo 3 rows in perf sheet: {len(df_combo3)}\n\n")
    if len(df_combo3) > 0:
        cols = ['Mã Phiếu', 'Barcode', 'Tên sản phẩm', 'Nơi nhận', 'Mã phiếu chuyển', 'Người chia hàng']
        f_out.write(df_combo3[cols].head(20).to_string() + "\n")
print("Done writing to inspect_perf_dua.txt")
