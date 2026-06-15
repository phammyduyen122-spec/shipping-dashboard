with open("app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for tableBody or updateTable in app.js...")
found = False
for i, line in enumerate(lines):
    if "updateTable" in line or "render" in line.lower() and "table" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
        found = True

# Let's search for the actual table row construction code
print("\nSearching for table HTML construction in app.js:")
for i, line in enumerate(lines):
    if "tr" in line and "td" in line and ("qtyReceived" in line or "slNhan" in line):
        print(f"Line {i+1}: {line.strip()}")
