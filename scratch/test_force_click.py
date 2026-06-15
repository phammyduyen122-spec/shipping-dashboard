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
            
            print("Locating 'Danh mục' form item...")
            # We want to find a form item or block with 'Danh mục' label
            # Let's search by text
            form_items = page.locator(".ant-form-item, div")
            # Let's use a selector that specifically matches the 'Danh mục' field
            # In the previous run, we saw label text 'Danh mục' and input 1, 2, 3, 4
            # Let's target the element with class '.ant-select-selector' inside the form item with 'Danh mục'
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            if await target_form_item.count() > 0:
                print("Target 'Danh mục' form item found!")
                select_box = target_form_item.locator(".ant-select-selector").first
                print("Clicking select box with force=True...")
                await select_box.click(force=True)
            else:
                print("Target form item by label text not found, trying fallback...")
                select_box = page.locator(".ant-select-selector").first
                await select_box.click(force=True)
                
            await page.wait_for_timeout(4000)
            
            # Save screenshot of opened select dropdown
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_filters_open_force.png"
            await page.screenshot(path=screenshot_path)
            print(f"Saved screenshot with open dropdown to {screenshot_path}")
            
            # Let's query elements that might be tree select nodes or options
            selectors = [
                ".ant-select-tree-node-content-wrapper",
                ".ant-select-tree-title",
                ".ant-select-tree-checkbox",
                ".ant-select-item-option-content",
                ".ant-select-item",
                "[role='treeitem']",
                "[role='option']"
            ]
            
            for sel in selectors:
                elems = page.locator(sel)
                cnt = await elems.count()
                print(f"Selector '{sel}': found {cnt} elements.")
                if cnt > 0:
                    texts = []
                    for i in range(min(cnt, 30)):
                        txt = await elems.nth(i).inner_text()
                        if txt.strip():
                            texts.append(txt.strip())
                    print(f"  First 30 texts: {texts}")
                    
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
