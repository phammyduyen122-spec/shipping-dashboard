import subprocess
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting HTTP Server on port 8080...", flush=True)
server_proc = subprocess.Popen(
    ["python", "-m", "http.server", "8080"],
    cwd=os.getcwd()
)

print("Starting Keep Tunnel Alive script...", flush=True)
tunnel_proc = subprocess.Popen(
    ["python", "keep_tunnel_alive.py"],
    cwd=os.getcwd()
)

try:
    url_printed = ""
    while True:
        # Check if processes are alive
        if server_proc.poll() is not None:
            print("WARNING: HTTP Server died! Restarting...", flush=True)
            server_proc = subprocess.Popen(["python", "-m", "http.server", "8080"], cwd=os.getcwd())
            
        if tunnel_proc.poll() is not None:
            print("WARNING: Tunnel script died! Restarting...", flush=True)
            tunnel_proc = subprocess.Popen(["python", "keep_tunnel_alive.py"], cwd=os.getcwd())
        
        # Read the active url file if it exists and print it
        if os.path.exists("active_tunnel_url.txt"):
            try:
                with open("active_tunnel_url.txt", "r", encoding="utf-8") as f:
                    url = f.read().strip()
                    if url and url != url_printed:
                        print(f"👉 Current Active Tunnel URL: {url}", flush=True)
                        url_printed = url
            except Exception as e_url:
                pass
                
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping server and tunnel...", flush=True)
    server_proc.terminate()
    tunnel_proc.terminate()
