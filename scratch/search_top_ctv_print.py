import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('app.js', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for idx in range(2360, min(2480, len(lines))):
        print(f"{idx+1}: {lines[idx]}", end="")

if __name__ == '__main__':
    main()
