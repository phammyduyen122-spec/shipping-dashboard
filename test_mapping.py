import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Read shipping data
shipping_file = "transfer_04062026-140455.xlsx"
df_ship = pd.read_excel(shipping_file, header=0)

# Read performance data
perf_dir = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
perf_file = glob.glob(os.path.join(perf_dir, "*.xlsx"))[0]
df_perf = pd.read_excel(perf_file, sheet_name="Sheet 1")

print("Shipping columns:", df_ship.columns.tolist())
print("Perf columns:", df_perf.columns.tolist())

# Create sets of keys
ship_keys = set()
for idx, row in df_ship.iterrows():
    if row.get('Chi nhánh chuyển') == "KHO RAU CỦ":
        tc = str(row.get('Mã chuyển hàng', '')).strip()
        ic = str(row.get('Mã hàng', '')).strip()
        if tc and ic:
            ship_keys.add((tc, ic))
            
print(f"Shipping (KHO RAU CỦ) keys count: {len(ship_keys)}")

perf_keys = {}
for idx, row in df_perf.iterrows():
    mpc = str(row.get('Mã phiếu chuyển', '')).strip()
    bc = str(row.get('Barcode', '')).strip()
    nc = str(row.get('Người chia hàng', '')).strip()
    if mpc and bc and nc:
        perf_keys[(mpc, bc)] = nc

print(f"Performance keys count: {len(perf_keys)}")

# Let's count matches
matches = 0
for k in ship_keys:
    if k in perf_keys:
        matches += 1
        
print(f"Matches found: {matches} / {len(ship_keys)}")

# Print 5 sample matches
printed = 0
for k in ship_keys:
    if k in perf_keys:
        print(f"Match: Key {k} -> User: {perf_keys[k]}")
        printed += 1
        if printed >= 5:
            break
