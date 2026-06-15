import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Reading data.js...")
with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    print(f"Total transfers: {len(transfers)}")
    
    # Search for product
    target_sku = None
    for t in transfers:
        name = t.get('itemName', '').lower()
        if 'yamazaky' in name or 'yamazaki' in name or 'khoai tây' in name:
            print(f"Found match: Code: {t.get('itemCode')} | Name: {t.get('itemName')} | Unit: {t.get('unit')}")
            target_sku = t.get('itemCode')
            # break or print all
            
    if target_sku:
        print(f"\n--- Checking transfers for SKU {target_sku} ---")
        sku_transfers = [t for t in transfers if t.get('itemCode') == target_sku]
        print(f"Total transfers for this SKU: {len(sku_transfers)}")
        
        for t in sku_transfers:
            # We also run app.js link/status logic simulator on this transfer
            is_orig = t.get('fromBranch') == 'KHO RAU CỦ'
            is_corr = t.get('fromBranch') == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'
            
            qty_s = t.get('qtyShipped', 0.0)
            qty_r = t.get('qtyReceived', 0.0)
            supp = t.get('supplementQty', 0.0)
            
            # Capping
            if is_orig and qty_r > qty_s and qty_r != -1:
                qty_r = qty_s
                
            chenh_lech = qty_r - qty_s
            
            print(f"Date: {t.get('date')} | From: {t.get('fromBranch')} | To: {t.get('toBranch')} | Shipped: {qty_s} | Received: {qty_r} | Supp: {supp} | Code: {t.get('transferCode')}")
else:
    print("Failed to find initialTransfers")
