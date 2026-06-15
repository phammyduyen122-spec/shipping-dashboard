import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    correctives = [t for t in transfers if t.get('fromBranch') == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG']
    
    diff_count = 0
    in_transit_count = 0
    
    for c in correctives:
        s = c.get('qtyShipped', 0.0)
        r = c.get('qtyReceived', 0.0)
        supp = c.get('supplementQty', 0.0)
        
        if s != r:
            diff_count += 1
            if r == -1:
                in_transit_count += 1
                
        # Assert that supplementQty equals qtyShipped for all correctives to supermarkets
        is_to_kfm = c.get('toBranch', '').upper().startswith('KFM')
        expected = s if is_to_kfm else 0.0
        if abs(supp - expected) > 1e-5:
            print(f"Mismatch: Code: {c.get('transferCode')} | To: {c.get('toBranch')} | Shipped: {s} | Received: {r} | Supp: {supp} | Expected: {expected}")
            
    print(f"Total correctives: {len(correctives)}")
    print(f"Correctives with qtyShipped != qtyReceived: {diff_count}")
    print(f"Correctives in-transit (qtyReceived == -1): {in_transit_count}")
else:
    print("Failed to parse data.js")
