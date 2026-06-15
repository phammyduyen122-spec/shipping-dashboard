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
        
        # Switch to Tab 2 first
        print("Switching to Tab 2...")
        await page.click("#tabPerformanceReport")
        await page.wait_for_timeout(2000)
        
        # Now set dates in Tab 2
        print("Setting date range: 2026-06-08 to 2026-06-09...")
        await page.fill("#perfFilterStartDate", "2026-06-08")
        await page.eval_on_selector("#perfFilterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#perfFilterEndDate", "2026-06-09")
        await page.eval_on_selector("#perfFilterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(3000)
        
        # Get all rows in the summary table
        rows = await page.locator("#perfSummaryBody tr").all()
        print(f"\n--- TAB 2 SUMMARY TABLE ROWS ({len(rows)} rows) ---")
        yam_count = 0
        for i, row in enumerate(rows):
            cols = await row.locator("td").all_text_contents()
            row_text = " ".join(cols)
            if "yamazaki" in row_text.lower() or "sp001222" in row_text.lower() or "sp001988" in row_text.lower():
                yam_count += 1
                print(f"Row {i+1}: {cols}")
                
        print(f"Found {yam_count} Yamazaki rows in Tab 2 summary table.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
