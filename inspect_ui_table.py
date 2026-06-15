import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(5000)
        
        # 1. Read start/end dates
        start_date = await page.input_value("#filterStartDate")
        end_date = await page.input_value("#filterEndDate")
        print(f"Default filters: Start Date = {start_date}, End Date = {end_date}")
        
        # 2. Get the table rows
        rows = await page.locator("#tableBody tr").all()
        print(f"\n--- TAB 1 TABLE ROWS ({len(rows)} rows on current page) ---")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        # 3. Change dates to show all (08/06 and 09/06)
        print("\nChanging dates to 2026-06-08 to 2026-06-09...")
        await page.fill("#filterStartDate", "2026-06-08")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.locator("#filterStartDate").press("Enter")
        await page.wait_for_timeout(2000)
        
        # Read table rows again
        rows = await page.locator("#tableBody tr").all()
        print(f"\n--- TAB 1 TABLE ROWS AFTER DATE CHANGE ({len(rows)} rows) ---")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        # 4. Search for Yamazaki
        print("\nSearching for Yamazaki (itemCode: SP001988 or SP001222 or 'Yamazaki')...")
        await page.fill("#filterItemCode", "yamazaki")
        # trigger input event
        await page.locator("#filterItemCode").press("Enter")
        await page.wait_for_timeout(2000)
        
        rows = await page.locator("#tableBody tr").all()
        print(f"\n--- TAB 1 TABLE ROWS AFTER YAMAZAKI SEARCH ({len(rows)} rows) ---")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
