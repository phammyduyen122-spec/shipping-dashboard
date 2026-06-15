import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        try:
            print("Logging in to next.kingfood.co...")
            await page.goto("https://next.kingfood.co/", timeout=45000)
            await page.wait_for_timeout(2000)
            await page.fill("#normal_login_account", "SC015807")
            await page.fill("#normal_login_password", "Yuanxxinh@1202")
            await page.click("button[type='submit']")
            await page.wait_for_timeout(8000)
            
            print("Navigating to product list page...")
            await page.goto("https://next.kingfood.co/product-hada/product-list", timeout=45000)
            await page.wait_for_timeout(10000)
            
            token = await page.evaluate("localStorage.getItem('_token')")
            print("Extracted token.")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Fetch category metadata
            print("Fetching categories...")
            cat_response = await page.request.get(
                "https://api.kingfood.co/v1/categories/fulldata",
                headers=headers
            )
            
            categories = await cat_response.json()
            print("Categories list type:", type(categories))
            print("Number of categories:", len(categories))
            if len(categories) > 0:
                print("First item type:", type(categories[0]))
                print("First item data:")
                print(json.dumps(categories[0], indent=2, ensure_ascii=False)[:600])
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
