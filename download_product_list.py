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
            
            print("Waiting for dashboard loading...")
            await page.wait_for_timeout(10000)
            
            print("Navigating to product-hada list...")
            await page.goto("https://next.kingfood.co/product-hada/product-list", timeout=45000)
            
            print("Waiting 30 seconds for 'Đang tải dữ liệu variant' to finish...")
            await page.wait_for_timeout(30000)
            
            # Take screenshot after 30s
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_loaded.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await page.screenshot(path=screenshot_path)
            print(f"Saved loaded screenshot to {screenshot_path}")
            
            # Look for buttons on the page
            buttons = await page.locator("button").all_text_contents()
            print("Buttons found on the page:")
            for b in buttons:
                if b.strip():
                    print(f"  - {b.strip()}")
            
            # Look for any inputs/filters
            inputs = await page.locator("input").all()
            print(f"Inputs found: {len(inputs)}")
            for idx, inp in enumerate(inputs):
                placeholder = await inp.get_attribute("placeholder") or ""
                id_attr = await inp.get_attribute("id") or ""
                print(f"  Input {idx+1}: id={id_attr}, placeholder={placeholder}")
                
            # Print table headers if any
            headers = await page.locator("th").all_text_contents()
            if headers:
                print("Table headers found:")
                print(headers)
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
