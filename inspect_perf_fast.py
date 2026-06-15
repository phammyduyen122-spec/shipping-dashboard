import pandas as pd

f_path = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard/chi-tiet-chia-qua-canh_06062026.xlsx"
df = pd.read_excel(f_path, nrows=5)

with open("inspect_perf_fast.txt", "w", encoding="utf-8") as f_out:
    f_out.write("Columns:\n")
    f_out.write(str(df.columns.tolist()) + "\n\n")
    f_out.write("First 3 rows:\n")
    f_out.write(str(df.head(3).to_dict('records')) + "\n")
print("Done writing to inspect_perf_fast.txt")
