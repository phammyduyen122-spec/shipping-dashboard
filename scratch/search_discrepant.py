import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('app.js', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start = -1
    for i, l in enumerate(lines):
        if 'function getFilteredPerfDiscrepantData' in l:
            start = i
            break
            
    if start != -1:
        for idx in range(start, min(start + 120, len(lines))):
            print(f"{idx+1}: {lines[idx]}", end="")
    else:
        print("Function not found!")

if __name__ == '__main__':
    main()
