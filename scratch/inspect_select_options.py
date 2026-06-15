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
            
            print("Clicking on 'Danh mục' select container...")
            # Let's click the .ant-select-selector inside the first select
            select_selector = page.locator(".ant-select-selector").first
            await select_selector.click()
            await page.wait_for_timeout(5000)
            
            # Save screenshot of opened select dropdown
            screenshot_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/scratch/product_list_filters_open.png"
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
