import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\DUYEN\.gemini\antigravity\brain\dca284e8-02b6-49ff-9cf8-e32c87a805c0\.system_generated\logs\transcript.jsonl"

if not os.path.exists(transcript_path):
    print(f"Transcript file not found at: {transcript_path}")
    sys.exit(0)

print(f"Reading transcript from {transcript_path}...")
user_messages = []
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            step = json.loads(line)
            # Find steps of type USER_INPUT
            if step.get("type") == "USER_INPUT":
                user_messages.append(step.get("content", ""))
        except Exception as e:
            pass

print(f"Total user messages found: {len(user_messages)}")
print("\n--- Listing recent user messages containing rules, dates, or keywords ---")
for idx, msg in enumerate(user_messages):
    msg_lower = msg.lower()
    if any(k in msg_lower for k in ["rule", "7.6", "7/6", "07/06", "nhận", "chuyển", "bổ sung", "auto"]):
        print(f"[{idx}]: {msg.strip()}")
        print("-" * 40)
