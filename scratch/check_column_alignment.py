import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Let's extract headers of the three tables
def get_headers(table_id):
    # Find table with table_id or text
    # Or just find all th tags inside the respective table block
    match = re.search(rf'<table.*?(?:id="{table_id}"|id=\'{table_id}\'|tbody id="{table_id}").*?<thead>(.*?)</thead>', html, re.DOTALL)
    if not match:
        # Fallback to general table search near that ID
        pos = html.find(table_id)
        if pos != -1:
            thead_start = html.rfind("<thead>", 0, pos)
            thead_end = html.find("</thead>", thead_start)
            thead_content = html[thead_start:thead_end]
            return [t.strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', thead_content, re.DOTALL)]
        return []
    return [t.strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', match.group(1), re.DOTALL)]

print("=== Main Table (Tab 1) ===")
headers_tab1 = get_headers("tableBody")
print("Headers:", [re.sub(r'<[^>]+>', '', h).strip() for h in headers_tab1])

match_t1 = re.search(r'function renderTable\(\).*?tr\.innerHTML\s*=\s*`([^`]+)`', js, re.DOTALL)
if match_t1:
    cells_t1 = re.findall(r'<td[^>]*>(.*?)</td>', match_t1.group(1), re.DOTALL)
    print("Cells:", [c.strip() for c in cells_t1])
    print(f"Headers count: {len(headers_tab1)}, Cells count: {len(cells_t1)}")

print("\n=== Performance Summary Table (Tab 2) ===")
headers_tab2 = get_headers("perfSummaryBody")
print("Headers:", [re.sub(r'<[^>]+>', '', h).strip() for h in headers_tab2])

match_t2 = re.search(r'function renderPerfSummaryTable\(\).*?tr\.innerHTML\s*=\s*`([^`]+)`', js, re.DOTALL)
if match_t2:
    cells_t2 = re.findall(r'<td[^>]*>(.*?)</td>', match_t2.group(1), re.DOTALL)
    print("Cells:", [c.strip() for c in cells_t2])
    print(f"Headers count: {len(headers_tab2)}, Cells count: {len(cells_t2)}")

print("\n=== Performance Details Table (Tab 2) ===")
headers_tab3 = get_headers("perfTableBody")
print("Headers:", [re.sub(r'<[^>]+>', '', h).strip() for h in headers_tab3])

match_t3 = re.search(r'function renderPerfTable\(\).*?tr\.innerHTML\s*=\s*`([^`]+)`', js, re.DOTALL)
if match_t3:
    cells_t3 = re.findall(r'<td[^>]*>(.*?)</td>', match_t3.group(1), re.DOTALL)
    print("Cells:", [c.strip() for c in cells_t3])
    print(f"Headers count: {len(headers_tab3)}, Cells count: {len(cells_t3)}")
