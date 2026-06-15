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
            await page.wait_for_timeout(2000)
            
            # Click the option
            print("Clicking option 'Sản phẩm thường - Thuộc tính SP'...")
            await page.locator("text='Sản phẩm thường - Thuộc tính SP'").click()
            
            # Wait 15 seconds and see what's on the screen
            print("Waiting 15 seconds for dialogs/toasts...")
            await page.wait_for_timeout(15000)
            
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_after_click.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await page.screenshot(path=screenshot_path)
            print(f"Saved screenshot after click to {screenshot_path}")
            
            # Print page body text to see if there is a warning/notification
            body_text = await page.locator("body").inner_text()
            print("\nPage body text (first 500 chars):")
            print(body_text[:500])
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
