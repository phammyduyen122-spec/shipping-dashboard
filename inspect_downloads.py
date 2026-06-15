import os
import glob
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("All xlsx files and their modification times:")
files = glob.glob("**/*.xlsx", recursive=True) + glob.glob("*.xlsx")
# deduplicate
files = sorted(list(set(files)))
for f in files:
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
    print(f"  {f} | Size: {os.path.getsize(f) / 1024 / 1024:.2f} MB | Modified: {mtime}")
