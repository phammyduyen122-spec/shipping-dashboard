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
        await page.wait_for_timeout(3000)
        
        # Change dates to 2026-06-08 to 2026-06-09
        print("Setting date range: 2026-06-08 to 2026-06-09...")
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(2000)
        
        # 1. Search for SP001222
        print("\n--- SEARCHING FOR SP001222 (BÁNH HAWAII KHOAI TÂY 232G) ---")
        await page.fill("#filterItemCode", "SP001222")
        await page.wait_for_timeout(1000)
        await page.locator("#filterItemCode").press("Enter")
        await page.wait_for_timeout(2000)
        
        # Print pagination info
        pag_info = await page.inner_text("#paginationInfo")
        print(f"Pagination Info for SP001222: {pag_info}")
        
        # Print table rows on page 1
        rows = await page.locator("#tableBody tr").all()
        print(f"Page 1 Rows for SP001222:")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        # 2. Clear filters
        print("\nClearing filters...")
        await page.click("#clearFiltersBtn")
        await page.wait_for_timeout(1000)
        
        # Re-set date range (since clear filters resets dates to latest date)
        print("Re-setting date range: 2026-06-08 to 2026-06-09...")
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(1000)
        
        # 3. Search for SP001988
        print("\n--- SEARCHING FOR SP001988 (BÁNH HAWAII KHOAI TÂY NHO 235G) ---")
        await page.fill("#filterItemCode", "SP001988")
        await page.wait_for_timeout(1000)
        await page.locator("#filterItemCode").press("Enter")
        await page.wait_for_timeout(2000)
        
        # Print pagination info
        pag_info = await page.inner_text("#paginationInfo")
        print(f"Pagination Info for SP001988: {pag_info}")
        
        # Print table rows on page 1
        rows = await page.locator("#tableBody tr").all()
        print(f"Page 1 Rows for SP001988:")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
