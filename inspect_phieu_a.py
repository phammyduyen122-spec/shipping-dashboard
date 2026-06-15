import pandas as pd
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

df6 = pd.read_excel("transfer_2026-06-06.xlsx", header=0)
df7 = pd.read_excel("transfer_2026-06-07.xlsx", header=0)
df = pd.concat([df6, df7], ignore_index=True)
df.columns = [str(c).strip() for c in df.columns]

# Search for any row from KHO RAU CỦ that has _A in code or docs
krc_rows = df[df['Chi nhánh chuyển'] == 'KHO RAU CỦ']
print("Total KHO RAU CỦ rows:", len(krc_rows))

phieu_a_rows = krc_rows[
    krc_rows['Mã chuyển hàng'].fillna("").astype(str).str.contains("_A") |
    krc_rows['Chứng từ gốc'].fillna("").astype(str).str.contains("_A") |
    krc_rows['Chứng từ phát sinh'].fillna("").astype(str).str.contains("_A")
]

print("Total KHO RAU CỦ rows matching '_A':", len(phieu_a_rows))
if len(phieu_a_rows) > 0:
    print(phieu_a_rows['Đã hậu kiểm'].value_counts(dropna=False))
    print(phieu_a_rows[['Mã chuyển hàng', 'Chi nhánh nhận', 'Mã hàng', 'Tên hàng', 'Số lượng chuyển', 'Đã hậu kiểm', 'Trạng thái']].head(10))
