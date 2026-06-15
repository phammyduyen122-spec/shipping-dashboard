import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Listing all cards in index.html:")
in_card = False
card_lines = []
for i, line in enumerate(lines):
    if "class=\"stat-card" in line:
        in_card = True
        card_lines = [f"Line {i+1}: {line.strip()}"]
    elif in_card:
        card_lines.append(line.strip())
        if "</div>" in line and len(card_lines) > 5:
            print("\n".join(card_lines))
            print("-" * 50)
            in_card = False
