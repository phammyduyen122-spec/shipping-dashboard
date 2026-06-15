import json
import re

with open("data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract transfers and performance transfers
transfers_match = re.search(r"window.initialTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)
perf_match = re.search(r"window.performanceTransfers\s*=\s*(\[.*?\]);", content, re.DOTALL)

if transfers_match:
    transfers = json.loads(transfers_match.group(1))
    t_dates = set(t.get("date") for t in transfers)
    print(f"Transfers unique dates: {sorted(list(t_dates))}")
    print(f"Transfers count: {len(transfers)}")
else:
    print("No initialTransfers match")

if perf_match:
    perf = json.loads(perf_match.group(1))
    p_dates = set(p.get("ngayChuyen") for p in perf)
    print(f"Performance unique dates: {sorted(list(p_dates))}")
    print(f"Performance count: {len(perf)}")
else:
    print("No performanceTransfers match")
