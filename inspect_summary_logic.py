with open("app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for updateSummary or summary calculation in app.js...")
found = False
for i, line in enumerate(lines):
    if "updateSummary" in line or "card-" in line or "total" in line.lower() and "received" in line.lower() and "shipped" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
        found = True

print("\nLet's print the lines around the summary calculation:")
# Let's find where summary cards are updated. We will search for code that sets innerText or innerHTML of summary cards.
for i, line in enumerate(lines):
    if "totalShipped" in line or "totalReceived" in line or "totalShortage" in line or "totalSupplement" in line:
        print(f"Line {i+1}: {line.strip()}")
