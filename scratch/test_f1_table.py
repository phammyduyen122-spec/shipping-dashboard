import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1800, "height": 1000})
        page = await context.new_page()
        
        try:
            print("Navigating to http://localhost:8080...")
            await page.goto("http://localhost:8080", timeout=15000)
            await page.wait_for_timeout(3000)
            
            # Click Tab 2 (CTV Performance / Hiệu suất chia hàng)
            print("Clicking Tab 2...")
            await page.click("text=Hiệu suất chia hàng")
            await page.wait_for_timeout(3000)
            
            # Wait for F1 category table body to be populated
            print("Locating F1 Category table...")
            table_body = page.locator("#perfF1CategoryBody")
            await table_body.wait_for(state="attached", timeout=10000)
            
            # Check row count
            rows = await table_body.locator("tr").count()
            print(f"F1 Table populated with {rows} rows.")
            
            # Save screenshot of the F1 table
            screenshot_path = "scratch/f1_table_screenshot.png"
            # Scroll to make the F1 table visible
            await page.locator("text=Theo dõi hiệu suất phân loại theo Ngành Hàng").scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            
            # Capture the table card element
            table_card = page.locator(".table-card:has-text('Theo dõi hiệu suất phân loại theo Ngành Hàng')")
            await table_card.screenshot(path=screenshot_path)
            print(f"Saved F1 table screenshot to {screenshot_path}")
            
        except Exception as e:
            print(f"Error during F1 table test: {e}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
