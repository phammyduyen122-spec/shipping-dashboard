import re
import json

try:
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # nguoiChia values inside initialTransfers or performanceTransfers
    # Let's find matches for "nguoiChia": "..."
    names = set(re.findall(r'"nguoiChia"\s*:\s*"([^"]*)"', content))
    print("Unique nguoiChia names in data.js:")
    for n in sorted(list(names)):
        print(f"  - {n}")
except Exception as e:
    print(f"Error: {e}")
