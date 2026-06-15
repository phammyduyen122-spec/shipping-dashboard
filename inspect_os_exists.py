import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

perf_dir1 = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
perf_dir2 = "performance dashboard"

f1 = os.path.join(perf_dir1, "chi-tiet-chia-qua-canh_09062026.xlsx")
f2 = os.path.join(perf_dir2, "chi-tiet-chia-qua-canh_09062026.xlsx")

print("Checking paths:")
print(f"  f1: '{f1}' exists? {os.path.exists(f1)}")
print(f"  f2: '{f2}' exists? {os.path.exists(f2)}")
print(f"  f2 (abspath): '{os.path.abspath(f2)}' exists? {os.path.exists(os.path.abspath(f2))}")

# Check files in f2 directory
if os.path.exists(perf_dir2):
    print(f"\nFiles in '{perf_dir2}':")
    print(os.listdir(perf_dir2))
else:
    print(f"\nDirectory '{perf_dir2}' does not exist!")
