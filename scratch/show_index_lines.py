import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx in range(585, min(610, len(lines))):
        print(f"{idx+1}: {lines[idx]}", end="")

if __name__ == '__main__':
    main()
