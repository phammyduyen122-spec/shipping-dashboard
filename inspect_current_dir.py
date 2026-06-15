import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Current working directory:", os.getcwd())
print("Files in current directory:")
for f in sorted(os.listdir(".")):
    if f.endswith(".xlsx") or f.endswith(".js") or f.endswith(".py"):
        print(f"  {f} ({os.path.getsize(f) / 1024 / 1024:.2f} MB)")
