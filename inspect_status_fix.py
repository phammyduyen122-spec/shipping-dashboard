import json
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    print(f"Loaded {len(transfers)} transfers.")
    
    # Let's run the linking logic in Python
    originals = []
    correctives = []
    
    for t in transfers:
        from_b = t.get('fromBranch', '').strip().lower()
        to_b = t.get('toBranch', '').strip().lower()
        status = t.get('docStatus', '').strip().lower()
        
        if 'hủy' in status or 'huy' in status:
            continue
            
        if from_b == 'kho rau củ':
            qty_s = t.get('qtyShipped', 0.0)
            qty_r = t.get('qtyReceived', 0.0)
            if qty_r > qty_s and qty_r != -1:
                qty_r = qty_s
            originals.append({
                'id': t.get('id'),
                'date': t.get('date'),
                'fromBranch': t.get('fromBranch'),
                'toBranch': t.get('toBranch'),
                'itemCode': t.get('itemCode'),
                'itemName': t.get('itemName'),
                'unit': t.get('unit'),
                'qtyShipped': qty_s,
                'qtyReceived': qty_r,
                'generatedDoc': t.get('generatedDoc', ''),
                'matchedCorrectiveQty': 0.0
            })
        elif from_b == 'kho rau củ xử lý chênh lệch chuyển hàng':
            qty_s = t.get('qtyShipped', 0.0)
            correctives.append({
                'id': t.get('id'),
                'date': t.get('date'),
                'fromBranch': t.get('fromBranch'),
                'toBranch': t.get('toBranch'),
                'itemCode': t.get('itemCode'),
                'qtyShipped': qty_s,
                'qtyReceived': t.get('qtyReceived', 0.0),
                'transferCode': t.get('transferCode', ''),
                'isMerged': False
            })

    # Build corrective map
    corrective_map = {}
    for c in correctives:
        key = f"{c['toBranch'].strip().lower()}_{c['itemCode'].strip().lower()}"
        if key not in corrective_map:
            corrective_map[key] = []
        corrective_map[key].append(c)

    # Link
    for orig in originals:
        key = f"{orig['toBranch'].strip().lower()}_{orig['itemCode'].strip().lower()}"
        candidates = corrective_map.get(key)
        if candidates:
            # 1. Code match
            match = None
            if orig['generatedDoc']:
                orig_gen = orig['generatedDoc'].strip().lower()
                for c in candidates:
                    if not c['isMerged'] and c['transferCode']:
                        c_code = c['transferCode'].strip().lower()
                        if c_code in orig_gen:
                            match = c
                            break
            # 2. Date proximity match
            if not match and orig['qtyShipped'] > orig['qtyReceived']:
                try:
                    orig_date = datetime.strptime(orig['date'], '%Y-%m-%d')
                    for c in candidates:
                        if not c['isMerged']:
                            c_date = datetime.strptime(c['date'], '%Y-%m-%d')
                            diff_days = abs((c_date - orig_date).days)
                            if diff_days <= 3:
                                match = c
                                break
                except Exception as e:
                    pass
            if match:
                orig['matchedCorrectiveQty'] = match['qtyShipped']
                match['isMerged'] = True

    # Calculate status counts by date
    by_date = {}
    for t in originals:
        d = t['date']
        if d not in by_date:
            by_date[d] = {'Thiếu': 0, 'Hao hụt': 0, 'Đủ': 0, 'Dư': 0}
            
        qty_s = t['qtyShipped']
        qty_r = t['qtyReceived']
        
        if qty_r == -1:
            continue
            
        chenh_lech = qty_r - qty_s
        sl_bo_sung = t['matchedCorrectiveQty']
        chenh_lech_con_lai = chenh_lech + sl_bo_sung
        
        status = 'Đủ'
        if chenh_lech_con_lai < 0:
            unit = (t['unit'] or "").lower()
            if 'kg' in unit and qty_s > 0 and (abs(chenh_lech_con_lai) / qty_s) < 0.15:
                status = 'Hao hụt'
            else:
                status = 'Thiếu'
        elif chenh_lech_con_lai > 0:
            status = 'Dư'
            
        by_date[d][status] += 1

    print("\n--- Status Counts with Fix (No fallback to t.supplementQty) ---")
    for d in sorted(by_date.keys()):
        print(f"Date: {d}")
        for k, v in by_date[d].items():
            print(f"  {k}: {v}")
else:
    print("Failed to parse data.js")
