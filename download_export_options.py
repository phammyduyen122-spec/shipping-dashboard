import asyncio
import os
import sys
from playwright.async_api import async_playwright
import pandas as pd

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        try:
            print("Logging into next.kingfood.co...")
            await page.goto("https://next.kingfood.co/", timeout=45000)
            await page.wait_for_timeout(2000)
            
            await page.fill("#normal_login_account", "SC015807")
            await page.fill("#normal_login_password", "Yuanxxinh@1202")
            await page.click("button[type='submit']")
            await page.wait_for_timeout(10000)
            
            print("Navigating to product-hada list...")
            await page.goto("https://next.kingfood.co/product-hada/product-list", timeout=45000)
            await page.wait_for_timeout(30000)
            
            # Click "Xuất file"
            print("Clicking 'Xuất file' dropdown...")
            await page.click("button:has-text('Xuất file')")
            await page.wait_for_timeout(1500)
            
            # Click "Sản phẩm thường - Thuộc tính SP" and wait for download
            print("Clicking option 'Sản phẩm thường - Thuộc tính SP'...")
            async with page.expect_download(timeout=180000) as download_info:
                await page.locator("text='Sản phẩm thường - Thuộc tính SP'").click()
            download = await download_info.value
            
            target_path = "attributes.xlsx"
            await download.save_as(target_path)
            print(f"🎉 Downloaded product attributes to {target_path}")
            
            # Inspect the Excel columns
            df = pd.read_excel(target_path, nrows=5)
            print("\nExcel Columns in attributes.xlsx:")
            print(list(df.columns))
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
