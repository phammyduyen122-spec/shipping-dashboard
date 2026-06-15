import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        try:
            print("Logging in...")
            await page.goto("https://next.kingfood.co/", timeout=45000)
            await page.wait_for_timeout(2000)
            await page.fill("#normal_login_account", "SC015807")
            await page.fill("#normal_login_password", "Yuanxxinh@1202")
            await page.click("button[type='submit']")
            await page.wait_for_timeout(8000)
            
            print("Navigating to product list...")
            await page.goto("https://next.kingfood.co/product-hada/product-list", timeout=45000)
            await page.wait_for_timeout(15000)
            
            # Print table row counts
            rows = page.locator("tbody tr")
            print(f"Found {await rows.count()} rows in the table on initial load.")
            if await rows.count() > 0:
                print("First row text:")
                print(await rows.first.inner_text())
                
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_initial_load.png"
            await page.screenshot(path=screenshot_path)
            print(f"Saved initial load screenshot to {screenshot_path}")
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
