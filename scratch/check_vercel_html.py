import urllib.request
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://shipping-performance.vercel.app/"
print("Checking Vercel deployment...")
for i in range(12):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Cache-Control': 'no-cache'}
        )
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            if "app.js?v=112" in html:
                print("\nSuccess: Vercel deployment is LIVE with version v=112!")
                sys.exit(0)
            else:
                print(f"Attempt {i+1}: Version v=105 is not live yet. Retrying in 5 seconds...")
    except Exception as e:
        print("Error fetching URL:", e)
    time.sleep(5)
print("\nTimeout: Version v=105 is not live on Vercel yet.")
sys.exit(1)
