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
            
            # Find all divs that are visible and check their class names
            all_divs = await page.locator("div").all()
            print(f"Total divs on page: {len(all_divs)}")
            
            dropdowns = []
            for d in all_divs:
                cls = await d.get_attribute("class") or ""
                if "dropdown" in cls.lower() or "select" in cls.lower() or "tree" in cls.lower():
                    # Check if visible
                    if await d.is_visible():
                        dropdowns.append((cls, await d.inner_html()))
                        
            print(f"Found {len(dropdowns)} visible dropdown/select/tree related divs:")
            for idx, (cls, html) in enumerate(dropdowns):
                print(f"  Div {idx+1} class: '{cls}'")
                # Print some child tags
                # Let's parse classes inside this div
                print(f"    Length of HTML: {len(html)}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
