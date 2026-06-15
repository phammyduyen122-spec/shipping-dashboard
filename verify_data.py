import json
import re

print("Reading data.js...")
with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract initialTransfers JSON using regex
m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    print(f"Total transfers in data.js: {len(transfers)}")
    
    # Filter for June 7 and 8
    jun7 = [t for t in transfers if t.get('date') == '2026-06-07']
    jun8 = [t for t in transfers if t.get('date') == '2026-06-08']
    
    print(f"Transfers for 2026-06-07: {len(jun7)}")
    print(f"Transfers for 2026-06-08: {len(jun8)}")
    
    # Check if nguoiChia is populated
    jun7_with_divider = [t for t in jun7 if t.get('nguoiChia')]
    jun8_with_divider = [t for t in jun8 if t.get('nguoiChia')]
    
    print(f"2026-06-07 transfers with Divider Staff: {len(jun7_with_divider)} / {len(jun7)}")
    print(f"2026-06-08 transfers with Divider Staff: {len(jun8_with_divider)} / {len(jun8)}")
    
    if jun8_with_divider:
        print("Sample June 8 Divider mapping:")
        for t in jun8_with_divider[:5]:
            print(f"  TransferCode: {t.get('transferCode')}, ItemCode: {t.get('itemCode')}, NguoiChia: {t.get('nguoiChia')}")
else:
    print("Could not parse window.initialTransfers from data.js")
