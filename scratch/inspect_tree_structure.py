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
            
            print("Opening select...")
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            await target_form_item.locator(".ant-select-selector").first.click(force=True)
            await page.wait_for_timeout(3000)
            
            # Find the tree nodes
            nodes = page.locator(".ant-select-tree-treenode")
            count = await nodes.count()
            print(f"Found {count} tree nodes.")
            
            for i in range(count):
                node = nodes.nth(i)
                text = await node.locator(".ant-select-tree-node-content-wrapper").inner_text()
                # Print the structure of this node
                # Find if there is a switcher
                switcher = node.locator(".ant-select-tree-switcher")
                switcher_count = await switcher.count()
                print(f"Node {i+1}: text='{text.strip()}', has_switcher={switcher_count > 0}")
                
                # If it is '1.BAKERY AND DELICA' or '1.FRESH FOOD', let's click its switcher to expand it
                if any(x in text for x in ['1.BAKERY AND DELICA', '1.FRESH FOOD']):
                    print(f"  -> Clicking switcher to expand '{text.strip()}'...")
                    await switcher.first.click(force=True)
                    await page.wait_for_timeout(1000)
            
            print("After expansion, let's look at all visible titles:")
            titles = await page.locator(".ant-select-tree-title").all_text_contents()
            print("Visible tree titles:")
            for idx, t in enumerate(titles):
                print(f"  - {t.strip()}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
