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
            
            print("Clicking 'Xuất file' dropdown...")
            await page.click("button:has-text('Xuất file')")
            await page.wait_for_timeout(2000)
            
            # Print all dropdown elements
            dropdown_elems = page.locator(".ant-dropdown-menu-item, [role='menuitem'], li")
            cnt = await dropdown_elems.count()
            print(f"Found {cnt} dropdown menu elements:")
            for idx in range(cnt):
                txt = await dropdown_elems.nth(idx).inner_text()
                if txt.strip():
                    print(f"  - Option {idx+1}: '{txt.strip()}'")
                    
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
