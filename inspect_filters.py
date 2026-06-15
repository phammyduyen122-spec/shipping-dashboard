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
            
            # Click the filter funnel icon
            # Let's locate the button with the filter icon. In the screenshot, it's next to the eye icon.
            # It's an ant-btn or a button near the search input
            print("Locating and clicking filter funnel icon...")
            # Let's find all buttons and check which one is the funnel. The funnel button has an icon inside.
            # We can select it by class or icon
            filter_button = page.locator("button .anticon-filter, button:has(svg), .anticon-filter").first
            if await filter_button.count() > 0:
                await filter_button.click()
                print("Clicked filter button.")
            else:
                # Try clicking by index or selector
                print("Filter button icon locator not found, trying general selector...")
                await page.locator("button").nth(2).click() # The third button usually
            
            await page.wait_for_timeout(5000)
            
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_filters.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await page.screenshot(path=screenshot_path)
            print(f"Saved screenshot with filter panel to {screenshot_path}")
            
            # Print page text to see if filter options are open
            body_text = await page.locator("body").inner_text()
            print("\nPage body text (first 600 chars):")
            print(body_text[:600])
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
