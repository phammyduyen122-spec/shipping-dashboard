import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Searching for xlsx files recursively...")
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".xlsx"):
            full_path = os.path.join(root, f)
            print(f"Found: {full_path} ({os.path.getsize(full_path) / 1024 / 1024:.2f} MB)")
