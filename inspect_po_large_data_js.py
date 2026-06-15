import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Reading data.js...")
with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"window\.performanceTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    perf = json.loads(m.group(1))
    print(f"Total performance transfers: {len(perf)}")
    
    glitched = [p for p in perf if p.get('slRo', 0) > 1000 or p.get('slKien', 0) > 1000]
    print(f"Number of performance transfers with slRo or slKien > 1000: {len(glitched)}")
    
    for g in glitched:
        print(f"Code: {g.get('maPhieuChuyen')} | Barcode: {g.get('barcode')} | slRo: {g.get('slRo')} | slKien: {g.get('slKien')} | User: {g.get('nguoiChia')}")
        
    po_check = [p for p in perf if p.get('maPhieuChuyen') == 'PT1398729']
    print(f"\nTotal rows in data.js for PO PT1398729: {len(po_check)}")
    if po_check:
        print("Sample rows for PT1398729 in data.js:")
        for p in po_check[:5]:
            print(f"  Code: {p.get('maPhieuChuyen')} | Barcode: {p.get('barcode')} | slRo: {p.get('slRo')} | slKien: {p.get('slKien')} | User: {p.get('nguoiChia')}")
else:
    print("Could not find performanceTransfers in data.js")
