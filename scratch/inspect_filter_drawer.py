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
            
            # Find elements inside the filter drawer
            # Check for drawer containers (e.g. .ant-drawer, .ant-modal, form)
            drawer = page.locator(".ant-drawer, .ant-modal, form").first
            if await drawer.count() > 0:
                print("Drawer/Form found!")
                labels = await drawer.locator("label, .ant-form-item-label").all_text_contents()
                print("Labels found in drawer:")
                for l in labels:
                    if l.strip():
                        print(f"  - {l.strip()}")
                
                inputs = await drawer.locator("input, .ant-select").all()
                print(f"Inputs/Selects found: {len(inputs)}")
                for idx, inp in enumerate(inputs):
                    placeholder = await inp.get_attribute("placeholder") or ""
                    id_attr = await inp.get_attribute("id") or ""
                    cls = await inp.get_attribute("class") or ""
                    val = await inp.get_attribute("value") or ""
                    print(f"  Input {idx+1}: id={id_attr}, placeholder={placeholder}, class={cls[:40]}, value={val}")
            else:
                print("Drawer/Form container not found!")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
