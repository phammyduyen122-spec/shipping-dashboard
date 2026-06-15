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
            
            print("Clicking filter funnel button...")
            filter_button = page.locator("button .anticon-filter, button:has(svg), .anticon-filter").first
            await filter_button.click()
            await page.wait_for_timeout(3000)
            
            print("Clicking on 'Danh mục' input...")
            # Click the search input of the first select
            await page.click("#rc_select_1")
            await page.wait_for_timeout(1000)
            
            print("Typing '2.EGGS'...")
            await page.fill("#rc_select_1", "2.EGGS")
            await page.wait_for_timeout(2000)
            
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_after_click.png"
            await page.screenshot(path=screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")
            
            # Print any active dropdown classes/content
            dropdown_items = await page.locator(".ant-select-item, .ant-tree-select-dropdown, .ant-select-dropdown, [role='treeitem'], [role='option']").all()
            print(f"Found {len(dropdown_items)} dropdown items/options.")
            for idx, item in enumerate(dropdown_items[:20]):
                txt = await item.inner_text()
                cls = await item.get_attribute("class") or ""
                role = await item.get_attribute("role") or ""
                print(f"  Item {idx+1}: role={role}, class={cls[:40]}, text='{txt.strip()}'")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
