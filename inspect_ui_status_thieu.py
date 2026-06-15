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
        await page.wait_for_timeout(1000)
        
        # Select status 'Thiếu'
        print("Selecting status filter: 'Thiếu'...")
        await page.click("#filterStatusContainer .multiselect-select")
        await page.wait_for_timeout(500)
        await page.check("#filterStatusContainer input[value='Thiếu']")
        await page.wait_for_timeout(500)
        await page.click("body") # close dropdown
        await page.wait_for_timeout(1000)
        
        # 1. Search for SP001222
        print("\n--- SEARCHING FOR SP001222 WITH STATUS 'THIẾU' ---")
        await page.fill("#filterItemCode", "SP001222")
        await page.wait_for_timeout(2000)
        await page.click("#itemDropdownList span:has-text('SP001222')")
        await page.wait_for_timeout(500)
        await page.click("#btnConfirmSuggestions")
        await page.wait_for_timeout(2000)
        
        # Print pagination info and rows
        pag_info = await page.inner_text("#paginationInfo")
        print(f"Pagination Info: {pag_info}")
        rows = await page.locator("#tableBody tr").all()
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        # 2. Clear item filter only (by clicking the tag close button)
        print("\nClearing item tags...")
        await page.click("#clearFiltersBtn") # actually clear filters clears all including status, so let's reset status
        await page.wait_for_timeout(1000)
        
        # Re-set dates and status
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(500)
        await page.click("#filterStatusContainer .multiselect-select")
        await page.wait_for_timeout(500)
        await page.check("#filterStatusContainer input[value='Thiếu']")
        await page.wait_for_timeout(500)
        await page.click("body")
        await page.wait_for_timeout(1000)
        
        # 3. Search for SP001988
        print("\n--- SEARCHING FOR SP001988 WITH STATUS 'THIẾU' ---")
        await page.fill("#filterItemCode", "SP001988")
        await page.wait_for_timeout(2000)
        await page.click("#itemDropdownList span:has-text('SP001988')")
        await page.wait_for_timeout(500)
        await page.click("#btnConfirmSuggestions")
        await page.wait_for_timeout(2000)
        
        # Print pagination info and rows
        pag_info = await page.inner_text("#paginationInfo")
        print(f"Pagination Info: {pag_info}")
        rows = await page.locator("#tableBody tr").all()
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
