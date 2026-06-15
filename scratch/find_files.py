import os

search_paths = [
    "C:\\Users\\DUYEN\\Downloads",
    "C:\\Users\\DUYEN\\Desktop",
    "C:\\Users\\DUYEN\\Documents",
    "C:\\Users\\DUYEN\\.gemini\\antigravity\\scratch\\shipping-dashboard",
    "C:\\Users\\DUYEN\\.gemini\\antigravity\\scratch\\shipping-dashboard\\scratch",
    "C:\\Users\\DUYEN\\.gemini\\antigravity\\brain\\dca284e8-02b6-49ff-9cf8-e32c87a805c0\\scratch",
]

target_patterns = [
    "transfer_10062026-181446",
    "chi-tiet-chia-qua-canh_10062026"
]

print("=== Searching for files ===")
for path in search_paths:
    if not os.path.exists(path):
        continue
    print(f"Checking: {path}")
    try:
        for f in os.listdir(path):
            for pattern in target_patterns:
                if pattern.lower() in f.lower():
                    print(f"Found: {os.path.join(path, f)}")
    except Exception as e:
        print(f"Error checking {path}: {e}")
