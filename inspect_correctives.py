import pandas as pd
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load transfer_2026-06-07.xlsx and transfer_2026-06-06.xlsx
df6 = pd.read_excel("transfer_2026-06-06.xlsx", header=0)
df7 = pd.read_excel("transfer_2026-06-07.xlsx", header=0)

df = pd.concat([df6, df7], ignore_index=True)
df.columns = [str(c).strip() for c in df.columns]

# Filter rows from KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG
correctives = df[df['Chi nhánh chuyển'] == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
print("Total corrective rows in df6 & df7:", len(correctives))

# Let's inspect counts of different columns
print("\nUnique values in 'Đã hậu kiểm' for corrective rows:")
print(correctives['Đã hậu kiểm'].value_counts(dropna=False))

# Let's see how many have daHauKiem == 'Không' and their codes
print("\nSample of corrective rows with daHauKiem == 'Không':")
print(correctives[correctives['Đã hậu kiểm'].str.lower().str.strip() == 'không'][['Mã chuyển hàng', 'Chi nhánh nhận', 'Mã hàng', 'Tên hàng', 'Số lượng chuyển', 'Chứng từ gốc', 'Trạng thái']].head(20))
