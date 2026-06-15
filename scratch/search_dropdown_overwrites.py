import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('app.js', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, l in enumerate(lines):
        if 'filterCategoryOptions' in l or 'perfFilterCategoryOptions' in l:
            print(f"{i+1}: {l.strip()}")

if __name__ == '__main__':
    main()
