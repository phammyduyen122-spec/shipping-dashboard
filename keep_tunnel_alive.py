import subprocess
import time
import re
import sys

def run_tunnel():
    sys.stdout.reconfigure(encoding='utf-8')
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8080", "nokey@localhost.run"]
    while True:
        print("Starting SSH tunnel...", flush=True)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8', errors='ignore')
        
        for line in iter(proc.stdout.readline, ''):
            clean_line = line.strip()
            print(f"TUNNEL: {clean_line}", flush=True)
            if "lhr.life" in clean_line or "lhr.rocks" in clean_line:
                match = re.search(r'https://[a-zA-Z0-9\.]+\.lhr\.(?:life|rocks|rocks/|life/)', clean_line)
                if match:
                    url = match.group(0).rstrip('/')
                    print(f"🎉 ACTIVE TUNNEL URL: {url}", flush=True)
                    with open("active_tunnel_url.txt", "w", encoding='utf-8') as f:
                        f.write(url)
        
        proc.wait()
        print(f"Tunnel process exited with code: {proc.returncode}. Restarting in 5 seconds...", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    run_tunnel()
