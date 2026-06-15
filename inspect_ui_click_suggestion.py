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
        
        # Type 'yamazaky' (with 'y') and press Enter without checking checkboxes
        print("\n--- SEARCHING FOR 'yamazaky' (WITH 'y') AND PRESSING ENTER ---")
        await page.fill("#filterItemCode", "yamazaky")
        await page.wait_for_timeout(1000)
        await page.locator("#filterItemCode").press("Enter")
        await page.wait_for_timeout(2000)
        
        # Print selected tags to see if they were added
        tags = await page.locator("#itemTagsContainer .tag-label").all_text_contents()
        print(f"Selected item tags in UI: {tags}")
        
        # Print pagination info
        pag_info = await page.inner_text("#paginationInfo")
        print(f"Pagination Info: {pag_info}")
        
        # Filter status: Thiếu
        print("\nSelecting status filter: 'Thiếu'...")
        await page.click("#filterStatusContainer .multiselect-select")
        await page.wait_for_timeout(500)
        await page.check("#filterStatusContainer input[value='Thiếu']")
        await page.wait_for_timeout(500)
        await page.click("body")
        await page.wait_for_timeout(2000)
        
        # Print all shortage rows currently in table (since we filtered by yamazaky and status Thiếu)
        rows = await page.locator("#tableBody tr").all()
        print(f"\n--- TABLE ROWS WITH STATUS 'THIẾU' ---")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
