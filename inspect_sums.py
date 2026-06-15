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
    
    by_date = {}
    for t in transfers:
        d = t.get('date')
        if d not in by_date:
            by_date[d] = {
                'shipped': 0.0,
                'received': 0.0,
                'supplement': 0.0,
                'rows': 0,
                'orig_shipped': 0.0,
                'orig_received': 0.0,
                'corr_shipped': 0.0,
                'corr_received': 0.0,
                'corr_supplement': 0.0,
                'num_orig': 0,
                'num_corr': 0
            }
        
        qty_s = t.get('qtyShipped', 0.0)
        qty_r = t.get('qtyReceived', 0.0)
        supp = t.get('supplementQty', 0.0)
        
        # We only count received if not -1 for original
        is_orig = t.get('fromBranch') == 'KHO RAU CỦ'
        
        by_date[d]['rows'] += 1
        if is_orig:
            by_date[d]['num_orig'] += 1
            by_date[d]['orig_shipped'] += qty_s
            if qty_r != -1:
                by_date[d]['orig_received'] += qty_r
        else:
            by_date[d]['num_corr'] += 1
            by_date[d]['corr_shipped'] += qty_s
            if qty_r != -1:
                by_date[d]['corr_received'] += qty_r
            by_date[d]['corr_supplement'] += supp

    print("\nSummary by Date:")
    for d in sorted(by_date.keys()):
        stats = by_date[d]
        orig_shipped = stats['orig_shipped']
        orig_received = stats['orig_received']
        orig_shortage = orig_shipped - orig_received
        corr_supp = stats['corr_supplement']
        remaining = orig_shortage - corr_supp
        
        print(f"Date: {d}")
        print(f"  Total Rows: {stats['rows']} (Originals: {stats['num_orig']}, Correctives: {stats['num_corr']})")
        print(f"  Original Shipped: {orig_shipped:.2f}")
        print(f"  Original Received: {orig_received:.2f}")
        print(f"  Original Shortage (Shipped - Received): {orig_shortage:.2f}")
        print(f"  Corrective Supplement: {corr_supp:.2f}")
        print(f"  Remaining Shortage (Shortage - Supp): {remaining:.2f}")
else:
    print("Failed to find initialTransfers in data.js")
