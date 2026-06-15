import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f = "transfer_09062026-165346.xlsx"
df_raw = pd.read_excel(f, header=None, nrows=10)
header_row = 0
for idx in range(len(df_raw)):
    row_vals = [str(x).lower() for x in df_raw.iloc[idx].values]
    if any('mã hàng' in x for x in row_vals) or any('tên hàng' in x for x in row_vals):
        header_row = idx
        break
df = pd.read_excel(f, header=header_row)
df.columns = [str(c).strip() for c in df.columns]

from_col = [c for c in df.columns if 'chuyển' in c.lower() and 'nhánh' in c.lower() or 'nơi chuyển' in c.lower() or 'chi nhánh chuyển' in c.lower()][0]
to_col = [c for c in df.columns if 'nhận' in c.lower() and 'nhánh' in c.lower() or 'nơi nhận' in c.lower() or 'chi nhánh nhận' in c.lower()][0]
code_col = [c for c in df.columns if 'mã hàng' in c.lower() or 'mã' in c.lower() and 'hàng' in c.lower()][0]
name_col = [c for c in df.columns if 'tên hàng' in c.lower() or 'tên' in c.lower() and 'hàng' in c.lower()][0]
shipped_col = [c for c in df.columns if 'chuyển' in c.lower() and 'lượng' in c.lower()][0]
received_col = [c for c in df.columns if 'nhận' in c.lower() and 'lượng' in c.lower()][0]
date_col = [c for c in df.columns if 'ngày' in c.lower()][0]
code_trans = [c for c in df.columns if 'mã chuyển hàng' in c.lower() or 'mã' in c.lower() and 'chuyển' in c.lower() and 'hàng' in c.lower()][0]
orig_doc_col = [c for c in df.columns if 'chứng từ gốc' in c.lower() or 'chứng từ' in c.lower() and 'gốc' in c.lower()][0]
gen_doc_col = [c for c in df.columns if 'chứng từ phát sinh' in c.lower() or 'chứng từ' in c.lower() and 'phát sinh' in c.lower()][0]

df[shipped_col] = pd.to_numeric(df[shipped_col], errors='coerce').fillna(0).astype(float)
df[received_col] = pd.to_numeric(df[received_col], errors='coerce').fillna(0).astype(float)

# Filter for the Yamazaki codes
codes = ['SP001222', 'SP001988']
df_yam = df[df[code_col].astype(str).str.strip().isin(codes)]

# 1. Shortage rows (KHO RAU CU, received < shipped)
df_orig = df_yam[df_yam[from_col].astype(str).str.strip() == 'KHO RAU CỦ']
shortages = df_orig[df_orig[received_col] < df_orig[shipped_col]]
print(f"Total original transfer rows for Yamazaki: {len(df_orig)}")
print(f"Total shortage rows for Yamazaki: {len(shortages)}")
if not shortages.empty:
    for idx, r in shortages.iterrows():
        print(f"SHORTAGE | Date: {r[date_col]} | To: {r[to_col]} | Code: {r[code_col]} | Shipped: {r[shipped_col]} | Received: {r[received_col]} | Trans: {r[code_trans]} | GenDoc: {r[gen_doc_col]}")

# 2. Correctives (KHO RAU CU XU LY CHENH LECH CHUYEN HANG)
df_corr = df_yam[df_yam[from_col].astype(str).str.strip() == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
print(f"\nTotal corrective transfer rows for Yamazaki: {len(df_corr)}")
if not df_corr.empty:
    for idx, r in df_corr.iterrows():
        print(f"CORRECTIVE | Date: {r[date_col]} | To: {r[to_col]} | Code: {r[code_col]} | Shipped: {r[shipped_col]} | Received: {r[received_col]} | Trans: {r[code_trans]} | OrigDoc: {r[orig_doc_col]}")

# 3. Check what's inside data.js for these shortages
import json
print("\n--- CHECKING DATA.JS RECORDS ---")
with open("data.js", "r", encoding="utf-8") as js_f:
    lines = js_f.readlines()
transfers_line = [line for line in lines if 'window.initialTransfers =' in line][0]
transfers_data = json.loads(transfers_line.replace('window.initialTransfers =', '').strip().rstrip(';'))

yam_js = [t for t in transfers_data if t['itemCode'] in codes]
print(f"Total Yamazaki records in data.js: {len(yam_js)}")

# Print shortage/corrective records from data.js
for t in yam_js:
    # Check if this record has a difference
    qtyRec = t['qtyReceived']
    qtyShip = t['qtyShipped']
    fromBranch = t['fromBranch']
    
    if (fromBranch == 'KHO RAU CỦ' and qtyRec < qtyShip) or (fromBranch == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'):
        print(f"JS_REC | Date: {t['date']} | From: {t['fromBranch']} | To: {t['toBranch']} | Code: {t['itemCode']} | Shipped: {t['qtyShipped']} | Received: {t['qtyReceived']} | Trans: {t['transferCode']} | OrigDoc: {t['originalDoc']} | GenDoc: {t['generatedDoc']} | matchedCorrectiveQty: {t.get('matchedCorrectiveQty', 0)}")
