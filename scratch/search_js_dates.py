import sys
import os

def search_in_file(filename, term):
    print(f"=== Searching for '{term}' in {filename} ===")
    if not os.path.exists(filename):
        print("File does not exist")
        return
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if term.lower() in line.lower():
            safe_line = line.strip().encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
            print(f"{idx+1}: {safe_line}")

search_in_file("app.js", "2026-06")
search_in_file("app.js", "09/06")
search_in_file("app.js", "defaultDate")
search_in_file("app.js", "maxDate")
search_in_file("app.js", "minDate")
search_in_file("app.js", "perfFilterStartDate")
