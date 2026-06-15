import sys

def check_brackets():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        content = open('app.js', 'r', encoding='utf-8').read()
        
        # Basic balance check for brackets/braces
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        lines = content.splitlines()
        
        for r_idx, line in enumerate(lines):
            for c_idx, char in enumerate(line):
                if char in '({[':
                    stack.append((char, r_idx+1, c_idx+1))
                elif char in ')}]':
                    if not stack:
                        print(f"Unmatched closing bracket '{char}' at line {r_idx+1}, col {c_idx+1}")
                        return False
                    top, r, c = stack.pop()
                    if top != mapping[char]:
                        print(f"Mismatched bracket: opened '{top}' at line {r}, col {c} but closed with '{char}' at line {r_idx+1}, col {c_idx+1}")
                        return False
                        
        if stack:
            top, r, c = stack[-1]
            print(f"Unclosed open bracket '{top}' at line {r}, col {c}")
            return False
            
        print("✅ Bracket balance check passed successfully!")
        return True
    except Exception as e:
        print(f"Error checking app.js: {e}")
        return False

if __name__ == '__main__':
    check_brackets()
