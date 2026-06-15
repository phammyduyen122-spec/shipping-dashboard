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
            
            # Click the "Xuất file" button
            print("Clicking 'Xuất file' dropdown button...")
            await page.click("button:has-text('Xuất file')")
            await page.wait_for_timeout(2000)
            
            # Take screenshot of the opened dropdown
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_export_dropdown.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await page.screenshot(path=screenshot_path)
            print(f"Saved dropdown screenshot to {screenshot_path}")
            
            # Print menu options elements text
            # Usually Ant Design or standard dropdown items are in list tags or divs with specific classes
            menu_items = await page.locator(".ant-dropdown-menu-item, .ant-select-item-option-content, li, [role='menuitem']").all_text_contents()
            print("Menu items or options found:")
            for item in menu_items:
                if item.strip():
                    print(f"  - {item.strip()}")
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
