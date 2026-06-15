import asyncio
import os
import sys
import csv
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        try:
            print("Navigating to http://localhost:8080...")
            await page.goto("http://localhost:8080", timeout=15000)
            await page.wait_for_timeout(3000)
            
            # 1. Test Tab 1 Shipping Export
            print("\nTesting Tab 1 Shipping Export...")
            async with page.expect_download(timeout=15000) as download_info:
                await page.click("#btnExport")
            download = await download_info.value
            path_tab1 = "scratch/test_export_tab1.csv"
            await download.save_as(path_tab1)
            print(f"Saved Tab 1 export to {path_tab1}")
            
            # Read first line of Tab 1 export
            with open(path_tab1, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                headers = next(reader)
                print("Tab 1 CSV Headers:", headers)
                print("Number of columns:", len(headers))
                
            # 2. Test Tab 2 Performance Export
            print("\nTesting Tab 2 Performance Export...")
            # Click Tab 2 ( CTV Performance / Hiệu suất chia hàng )
            # In index.html, let's find the Tab 2 selector.
            # Usually it's an element with class tab or similar. Let's see:
            # Let's inspect the page content to find the Tab 2 tab button.
            # Usually they are button elements in a nav bar or tab-headers.
            # Let's click the tab header containing "Hiệu suất" or similar.
            await page.click("text=Hiệu suất chia hàng")
            await page.wait_for_timeout(2000)
            
            async with page.expect_download(timeout=15000) as download_info:
                await page.click("#perfBtnExport")
            download = await download_info.value
            path_tab2 = "scratch/test_export_tab2.csv"
            await download.save_as(path_tab2)
            print(f"Saved Tab 2 export to {path_tab2}")
            
            # Read first line of Tab 2 export
            with open(path_tab2, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                headers = next(reader)
                print("Tab 2 CSV Headers:", headers)
                print("Number of columns:", len(headers))
                
        except Exception as e:
            print(f"Error during export tests: {e}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
