import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Reading data.js...")
with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract initialTransfers JSON using regex
m = re.search(r"window\.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
if m:
    transfers = json.loads(m.group(1))
    print(f"Total transfers in data.js: {len(transfers)}")
    
    matches = []
    for t in transfers:
        item_name = str(t.get('itemName', '')).lower()
        to_branch = str(t.get('toBranch', '')).lower()
        if "mận" in item_name and "hậu" in item_name and "mizuki" in to_branch:
            matches.append(t)
            
    print(f"Found {len(matches)} matches in data.js:")
    for t in matches:
        print(f"\nMatch:")
        for k, v in t.items():
            print(f"  {k}: {v}")
else:
    print("Could not parse window.initialTransfers from data.js")
