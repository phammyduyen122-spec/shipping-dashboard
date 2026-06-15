import json
import re

with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

transfers_match = re.search(r"window.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if transfers_match:
    transfers = json.loads(transfers_match.group(1))
    
    dates = ['2026-06-10', '2026-06-11']
    for d in dates:
        d_trans = [t for t in transfers if t.get("date") == d]
        with_nguoi_chia = [t for t in d_trans if t.get("nguoiChia")]
        total = len(d_trans)
        matched = len(with_nguoi_chia)
        print(f"Date: {d} | Total transfers: {total} | Matched with nguoiChia: {matched} ({matched/total*100:.2f}%)")
        
        # Print a sample of matched names if any
        if matched > 0:
            names = set(t.get("nguoiChia") for t in with_nguoi_chia[:10])
            print(f"  Sample names: {list(names)}")
else:
    print("No initialTransfers match")
