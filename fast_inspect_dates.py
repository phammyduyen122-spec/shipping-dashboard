import openpyxl
import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob("transfer_*.xlsx")):
    print(f"\nAnalyzing file: {f}")
    if not os.path.exists(f):
        print("  File does not exist")
        continue
    try:
        wb = openpyxl.load_workbook(f, read_only=True)
        sheet = wb.active
        print(f"  Active sheet: {sheet.title}")
        
        # Read header row
        header = []
        date_col_idx = None
        
        row_count = 0
        dates = set()
        
        for r_idx, row in enumerate(sheet.iter_rows(values_only=True)):
            if r_idx < 10 and not header:
                row_str = [str(x).lower() for x in row if x is not None]
                if any('mã hàng' in x for x in row_str) or any('tên hàng' in x for x in row_str):
                    header = [str(x).strip() for x in row]
                    for idx, h in enumerate(header):
                        if 'ngày' in h.lower():
                            date_col_idx = idx
                            print(f"  Header found at row {r_idx + 1}. Date column: '{h}' at index {date_col_idx}")
                            break
            elif header:
                row_count += 1
                if date_col_idx is not None and date_col_idx < len(row):
                    val = row[date_col_idx]
                    if val is not None:
                        dates.add(str(val))
                if row_count > 10000:
                    # just inspect up to 10k rows to be fast
                    break
        
        print(f"  Scanned {row_count} rows.")
        print(f"  Sample dates: {sorted(list(dates))[:10]}")
    except Exception as e:
        print(f"  Error: {e}")
