with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for metric card container elements in index.html...")
for i, line in enumerate(lines):
    if "card" in line.lower() or "shipped" in line.lower() or "received" in line.lower() or "shortage" in line.lower() or "supplement" in line.lower():
        if "id=" in line or "class=" in line:
            print(f"Line {i+1}: {line.strip()}")
