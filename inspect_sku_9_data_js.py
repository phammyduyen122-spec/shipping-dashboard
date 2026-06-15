import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    sku_transfers = [t for t in transfers if t.get('itemCode') == '1101392' and t.get('date') == '2026-06-09']
    
    print(f"Total transfers in data.js for SKU 1101392 on 2026-06-09: {len(sku_transfers)}")
    
    shortages = [t for t in sku_transfers if t.get('qtyReceived') < t.get('qtyShipped')]
    print(f"Shortage transfers in data.js for SKU 1101392 on 2026-06-09: {len(shortages)}")
    for s in shortages[:10]:
        print(f"  Code: {s.get('transferCode')} | To: {s.get('toBranch')} | Shipped: {s.get('qtyShipped')} | Received: {s.get('qtyReceived')} | Supp: {s.get('supplementQty')}")
else:
    print("Failed to parse data.js")
