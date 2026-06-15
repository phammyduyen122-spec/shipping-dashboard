import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Reading data.js for verification of the correct rules...")
with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    print(f"Total transfers in data.js: {len(transfers)}")
    
    # 1. Original rows check
    originals = [t for t in transfers if t.get('fromBranch') == 'KHO RAU CỦ']
    uncapped_orig = [o for o in originals if o.get('qtyReceived') > o.get('qtyShipped') and o.get('qtyReceived') != -1]
    print(f"Original transfers from KHO RAU CỦ: {len(originals)}")
    print(f"Number of original transfers with received > shipped (should be 0): {len(uncapped_orig)}")
    
    # 2. Corrective rows check
    correctives = [t for t in transfers if t.get('fromBranch') == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
    print(f"Corrective transfers from KRCXLCLCH: {len(correctives)}")
    
    # Categorize correctives
    to_kfm = [c for c in correctives if c.get('toBranch', '').upper().startswith('KFM')]
    to_warehouses = [c for c in correctives if not c.get('toBranch', '').upper().startswith('KFM')]
    
    print(f"  To Supermarkets (KFM): {len(to_kfm)}")
    print(f"  To Warehouses: {len(to_warehouses)}")
    
    # Rule validations for correctives
    kfm_valid = []
    for c in to_kfm:
        expected = 0.0 if c.get('qtyReceived') == -1 else c.get('qtyReceived')
        if c.get('supplementQty') == expected:
            kfm_valid.append(c)
            
    warehouses_ok = all(c.get('supplementQty') == 0 for c in to_warehouses)
    
    print(f"Rule validation: KFM supplementQty == qtyReceived (excluding -1): {len(kfm_valid)} / {len(to_kfm)}")
    print(f"Rule validation: Warehouse supplementQty == 0: {warehouses_ok}")
    
    if len(kfm_valid) == len(to_kfm) and warehouses_ok and len(uncapped_orig) == 0:
        print("🎉 SUCCESS: All data matches the correct business rules perfectly!")
    else:
        print("❌ ERROR: Some data did not match the rules.")
else:
    print("Could not parse transfers from data.js")
