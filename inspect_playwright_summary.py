import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser to inspect dashboard DOM content...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, timeout=30000, wait_until="load")
            await page.wait_for_timeout(3000) # wait for initialization
            
            # Print card contents
            card_ids = ["sumifsTotalShipped", "sumifsDuCount", "sumifsDuQty", "sumifsThieuCount", "sumifsThieuQty", "sumifsDuThieuCount", "sumifsDuThieuQty", "sumifsChuyenCount", "sumifsChuyenQty"]
            print("\n--- Summary Card Values ---")
            for cid in card_ids:
                el = page.locator(f"#{cid}")
                if await el.count() > 0:
                    text = await el.inner_text()
                    print(f"  {cid}: {text}")
                else:
                    print(f"  {cid}: Element not found!")
            
            # Print table row counts
            rows = page.locator("#tableBody tr")
            total_rows = await rows.count()
            print(f"\nTotal rows in main table: {total_rows}")
            
            # Print first 5 rows
            print("\n--- Sample Table Rows (First 5) ---")
            for i in range(min(5, total_rows)):
                row_text = await rows.nth(i).inner_text()
                print(f"  Row {i+1}: {repr(row_text.split(chr(9)))}") # split by tabs or spaces
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
