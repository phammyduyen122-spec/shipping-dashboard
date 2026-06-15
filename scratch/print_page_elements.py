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
            
            # Let's search for table-like elements
            selectors = [
                "table",
                ".ant-table",
                ".ant-table-tbody",
                ".ant-table-row",
                "tr",
                ".virtual-grid",
                ".virtual-table",
                ".ant-table-placeholder"
            ]
            
            for sel in selectors:
                cnt = await page.locator(sel).count()
                print(f"Selector '{sel}': found {cnt} elements.")
                
            # Print text of first few elements of .ant-table or table if found
            table_text = await page.locator(".ant-table, table").first.inner_text() if await page.locator(".ant-table, table").count() > 0 else "None"
            print("Table text (first 300 chars):")
            print(table_text[:300])
            
            # Check if there's any loading indicator
            spinners = await page.locator(".ant-spin, .loading, [class*='spin'], [class*='loading']").count()
            print(f"Spinners/loading elements found: {spinners}")
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
