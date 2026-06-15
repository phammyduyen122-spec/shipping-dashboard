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
            
            # Print checkboxes
            checkboxes = page.locator("input[type='checkbox'], .ant-checkbox, .ant-checkbox-input")
            cnt = await checkboxes.count()
            print(f"Found {cnt} checkboxes on the page:")
            for i in range(min(cnt, 20)):
                elem = checkboxes.nth(i)
                id_attr = await elem.get_attribute("id") or ""
                cls = await elem.get_attribute("class") or ""
                typ = await elem.get_attribute("type") or ""
                visible = await elem.is_visible()
                print(f"  Checkbox {i+1}: type={typ}, id={id_attr}, class={cls[:40]}, visible={visible}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
