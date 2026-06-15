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
        
        # Read total rows count and table content
        rows_count = await page.locator("#tableBody tr").count()
        print(f"Total rows in table after date change: {rows_count}")
        
        # Print first few rows to confirm dates are active
        print("Sample rows:")
        rows = await page.locator("#tableBody tr").all()
        for i, row in enumerate(rows[:5]):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        # Search for Yamazaki by typing into the input
        print("\nTyping 'Yamazaki' into item search...")
        await page.fill("#filterItemCode", "Yamazaki")
        await page.wait_for_timeout(2000)
        
        # Click the "Chọn tất cả kết quả gợi ý" checkbox
        print("Clicking suggestion select all checkbox...")
        selectAllSelector = "#itemDropdownList #suggestionSelectAll"
        if await page.locator(selectAllSelector).count() > 0:
            await page.click(selectAllSelector)
            await page.wait_for_timeout(500)
            
            # Click "Xác nhận chọn"
            print("Clicking 'Xác nhận chọn' button...")
            await page.click("#btnConfirmSuggestions")
            await page.wait_for_timeout(2000)
        else:
            print("Select all suggestions checkbox not found, trying enter...")
            await page.locator("#filterItemCode").press("Enter")
            await page.wait_for_timeout(2000)
            
        # Read table rows now
        rows = await page.locator("#tableBody tr").all()
        print(f"\n--- TABLE ROWS FOR YAMAZAKI ({len(rows)} rows) ---")
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            print(f"Row {i+1}: {cols}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
