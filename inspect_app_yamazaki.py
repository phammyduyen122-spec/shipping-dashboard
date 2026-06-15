import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def norm(s):
    return str(s or "").strip().lower()

# 1. Load data.js
with open("data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract window.initialTransfers
transfers_match = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\])\s*;", js_content, re.DOTALL)
if not transfers_match:
    print("Error: Could not parse window.initialTransfers from data.js")
    exit(1)
    
transfers = json.loads(transfers_match.group(1))
print(f"Loaded {len(transfers)} transfers from data.js.")

# 2. Implement linkTransfers in Python
originals = []
correctives = []

for t in transfers:
    status = norm(t.get('docStatus', ''))
    if 'hủy' in status or 'huy' in status:
        continue
        
    fromB = norm(t.get('fromBranch', ''))
    if fromB == "kho rau củ":
        qtyRec = float(t.get('qtyReceived', 0))
        qtyShip = float(t.get('qtyShipped', 0))
        if qtyRec > qtyShip and qtyRec != -1:
            qtyRec = qtyShip
        originals.append({
            **t,
            'qtyReceived': qtyRec,
            'matchedCorrectiveQty': 0
        })
    elif fromB == "kho rau củ xử lý chênh lệch chuyển hàng":
        correctives.append({
            **t,
            'isMerged': False
        })

corrective_map = {}
for c in correctives:
    key = f"{norm(c.get('toBranch', ''))}_{norm(c.get('itemCode', ''))}"
    if key not in corrective_map:
        corrective_map[key] = []
    corrective_map[key].append(c)

from datetime import datetime

for orig in originals:
    key = f"{norm(orig.get('toBranch', ''))}_{norm(orig.get('itemCode', ''))}"
    candidates = corrective_map.get(key)
    if candidates:
        match = None
        # 1. Try to match by code link
        if orig.get('generatedDoc'):
            orig_gen = norm(orig.get('generatedDoc'))
            for c in candidates:
                if c.get('isMerged'):
                    continue
                c_code = norm(c.get('transferCode'))
                if c_code != "" and c_code in orig_gen:
                    match = c
                    break
        
        # 2. Fallback: match by branch, item, date proximity
        if not match and (float(orig.get('qtyShipped', 0)) > float(orig.get('qtyReceived', 0))):
            try:
                orig_date = datetime.strptime(orig.get('date'), '%Y-%m-%d')
                for c in candidates:
                    if c.get('isMerged'):
                        continue
                    try:
                        c_date = datetime.strptime(c.get('date'), '%Y-%m-%d')
                        diff_days = abs((c_date - orig_date).days)
                        if diff_days <= 3 and float(c.get('qtyShipped', 0)) > 0:
                            match = c
                            break
                    except Exception as ex:
                        pass
            except Exception as ex:
                pass
                
        if match:
            orig['matchedCorrectiveQty'] = float(match.get('qtyShipped', 0))
            match['isMerged'] = True

processed_transfers = originals + correctives

# 3. Implement calculateStatus in Python
def calculate_status(t):
    slChuyenKRC = float(t.get('qtyShipped', 0))
    slNhanKRC = float(t.get('qtyReceived', 0))
    
    fromB = norm(t.get('fromBranch', ''))
    if fromB == "kho rau củ" and slNhanKRC > slChuyenKRC and slNhanKRC != -1:
        slNhanKRC = slChuyenKRC
        
    chenhLech = 0
    slBoSung = 0
    chenhLechConLai = 0
    statusText = "Đủ"
    
    if slNhanKRC == -1:
        return {
            'slChuyenKRC': slChuyenKRC,
            'slNhanKRC': slNhanKRC,
            'chenhLech': 0,
            'slBoSung': 0,
            'chenhLechConLai': 0,
            'statusText': "Đang chuyển"
        }
        
    toB = norm(t.get('toBranch', ''))
    isCorrective = fromB == "kho rau củ xử lý chênh lệch chuyển hàng"
    isSupermarket = toB.startswith("kfm")
    
    chenhLech = slNhanKRC - slChuyenKRC
    
    if isCorrective:
        slBoSung = slChuyenKRC if isSupermarket else 0
        chenhLechConLai = chenhLech
    else:
        slBoSung = float(t.get('matchedCorrectiveQty', 0))
        if chenhLech < 0:
            chenhLechConLai = chenhLech + slBoSung
        elif chenhLech > 0:
            chenhLechConLai = chenhLech - slBoSung
        else:
            chenhLechConLai = 0
            
    if chenhLechConLai < 0:
        unit = norm(t.get('unit', ''))
        if unit == 'kg' and slChuyenKRC > 0 and (abs(chenhLechConLai) / slChuyenKRC) < 0.15:
            statusText = "Hao hụt"
        else:
            statusText = "Thiếu"
    elif chenhLechConLai > 0:
        statusText = "Dư"
    else:
        statusText = "Đủ"
        
    return {
        'slChuyenKRC': slChuyenKRC,
        'slNhanKRC': slNhanKRC,
        'chenhLech': chenhLech,
        'slBoSung': slBoSung,
        'chenhLechConLai': chenhLechConLai,
        'statusText': statusText
    }

# Filter and print Yamazaki items
codes = ['sp001222', 'sp001988']
print("\n--- YAMAZAKI TRANSFERS REPORT ---")
count = 0
for t in processed_transfers:
    if norm(t.get('itemCode')) in codes:
        status = calculate_status(t)
        fromB = norm(t.get('fromBranch'))
        isShortage = fromB == "kho rau củ" and float(t.get('qtyReceived', 0)) < float(t.get('qtyShipped', 0))
        isCorrective = fromB == "kho rau củ xử lý chênh lệch chuyển hàng"
        
        if isShortage or isCorrective or float(t.get('matchedCorrectiveQty', 0)) > 0 or status['statusText'] != "Đủ":
            count += 1
            print(f"Date: {t.get('date')} | From: {t.get('fromBranch')} | To: {t.get('toBranch')}")
            print(f"  Trans: {t.get('transferCode')} | Code: {t.get('itemCode')} | Name: {t.get('itemName')}")
            print(f"  Excel Shipped: {t.get('qtyShipped')} | Excel Received: {t.get('qtyReceived')} | Matched corrective: {t.get('matchedCorrectiveQty', 0)}")
            print(f"  Calc: slChuyen={status['slChuyenKRC']} | slNhan={status['slNhanKRC']} | slBoSung={status['slBoSung']} | chenhLechConLai={status['chenhLechConLai']} | Status: {status['statusText']}")
            print("-" * 50)
            
print(f"Printed {count} abnormal/corrective records.")
