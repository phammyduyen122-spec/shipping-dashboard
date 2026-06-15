import re
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    tables = re.findall(r'<table.*?>.*?</table>', html, re.DOTALL)
    print(f"Found {len(tables)} tables in index.html\n")
    for idx, table in enumerate(tables):
        print(f"--- Table {idx+1} ---")
        headers = re.findall(r'<th.*?>(.*?)</th>', table, re.DOTALL)
        for h_idx, h in enumerate(headers):
            clean_h = re.sub(r'<.*?>', '', h).strip()
            print(f"  Col {h_idx+1}: {clean_h}")

if __name__ == '__main__':
    main()
