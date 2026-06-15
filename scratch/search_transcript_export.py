import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Open and scan the transcript.jsonl file
# Path: C:\Users\DUYEN\.gemini\antigravity\brain\dca284e8-02b6-49ff-9cf8-e32c87a805c0\.system_generated\logs\transcript.jsonl
log_path = r"C:\Users\DUYEN\.gemini\antigravity\brain\dca284e8-02b6-49ff-9cf8-e32c87a805c0\.system_generated\logs\transcript.jsonl"

try:
    with open(log_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if any(term in line.lower() for term in ["xuất file", "sản phẩm thường", "thuộc tính", "export"]):
                try:
                    data = json.loads(line)
                    content = data.get("content", "")
                    # print snippet
                    print(f"Line {idx} matches:")
                    print(f"  Type: {data.get('type')}, Source: {data.get('source')}")
                    print(f"  Content snippet: {content[:300]}")
                except Exception as e_json:
                    print(f"Line {idx} match (invalid JSON): {line[:300]}")
except Exception as e:
    print(f"Error reading transcript: {e}")
