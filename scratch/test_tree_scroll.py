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
            
            # Click switcher for '1.FRESH FOOD'
            print("Clicking switcher for '1.FRESH FOOD'...")
            switcher_fresh = page.locator(".ant-select-tree-treenode:has-text('1.FRESH FOOD') .ant-select-tree-switcher").first
            if await switcher_fresh.count() > 0:
                await switcher_fresh.click(force=True)
                await page.wait_for_timeout(2000)
                
            # Let's locate the scrollable holder
            holder = page.locator(".rc-virtual-list-holder").first
            if await holder.count() > 0:
                print("Holder found! Scrolling down...")
                # Scroll the holder
                await holder.evaluate("el => el.scrollTop = 200")
                await page.wait_for_timeout(2000)
                
                titles = await page.locator(".ant-select-tree-title").all_text_contents()
                print(f"Titles after scrolling scrollTop=200 ({len(titles)} found):")
                for t in titles:
                    print(f"  - {t.strip()}")
                    
                await holder.evaluate("el => el.scrollTop = 500")
                await page.wait_for_timeout(2000)
                
                titles = await page.locator(".ant-select-tree-title").all_text_contents()
                print(f"Titles after scrolling scrollTop=500 ({len(titles)} found):")
                for t in titles:
                    print(f"  - {t.strip()}")
            else:
                print("Holder not found!")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
