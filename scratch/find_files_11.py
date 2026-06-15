import os

downloads_dir = "C:\\Users\\DUYEN\\Downloads"
print(f"=== Searching for June 11th files in {downloads_dir} ===")
if os.path.exists(downloads_dir):
    for f in os.listdir(downloads_dir):
        if "11062026" in f or "11-06-2026" in f or "2026-06-11" in f:
            print(f"Found: {f}")
else:
    print("Downloads directory does not exist")
