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
            
            print("Opening 'Danh mục' tree select...")
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            await target_form_item.locator(".ant-select-selector").first.click(force=True)
            await page.wait_for_timeout(3000)
            
            # Click switcher for '1.BAKERY AND DELICA'
            print("Clicking switcher for '1.BAKERY AND DELICA'...")
            switcher_bakery = page.locator(".ant-select-tree-treenode:has-text('1.BAKERY AND DELICA') .ant-select-tree-switcher").first
            if await switcher_bakery.count() > 0:
                await switcher_bakery.click(force=True)
                await page.wait_for_timeout(1000)
                
            # Click switcher for '1.FRESH FOOD'
            print("Clicking switcher for '1.FRESH FOOD'...")
            switcher_fresh = page.locator(".ant-select-tree-treenode:has-text('1.FRESH FOOD') .ant-select-tree-switcher").first
            if await switcher_fresh.count() > 0:
                await switcher_fresh.click(force=True)
                await page.wait_for_timeout(1000)
                
            list_holder = page.locator(".ant-select-tree-list-holder").first
            target_cats = ["2.BAKERY", "2.DELICA", "2.EGGS", "2.FRUITS", "2.VEGETABLES"]
            
            for cat in target_cats:
                print(f"Searching for category: {cat}...")
                clicked = False
                # Scroll step-by-step to find it
                for scroll_top in range(0, 800, 50):
                    await list_holder.evaluate(f"el => el.scrollTop = {scroll_top}")
                    await page.wait_for_timeout(200)
                    
                    cat_elem = page.locator(f".ant-select-tree-treenode:has-text('{cat}') .ant-select-tree-node-content-wrapper").first
                    if await cat_elem.count() > 0 and await cat_elem.is_visible():
                        print(f"Found and clicking {cat} at scrollTop={scroll_top}...")
                        await cat_elem.click(force=True)
                        await page.wait_for_timeout(500)
                        clicked = True
                        break
                if not clicked:
                    print(f"❌ Failed to find and click category: {cat}!")
                    
            # Save screenshot
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_filters_clicked_robust.png"
            await page.screenshot(path=screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")
            
            # Print select box text to verify
            select_text = await target_form_item.locator(".ant-select-selector").inner_text()
            print("Select box text after robust selections:")
            print(select_text)
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
