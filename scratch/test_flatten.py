import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

def flatten_categories(cats_tree):
    flat = []
    for cat in cats_tree:
        if not isinstance(cat, list) or len(cat) < 2:
            continue
        cat_id = cat[0]
        cat_name = cat[1]
        flat.append({"id": cat_id, "name": cat_name})
        if len(cat) > 6 and isinstance(cat[6], list):
            flat.extend(flatten_categories(cat[6]))
    return flat

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
            
            print("Navigating...")
            await page.goto("https://next.kingfood.co/product-hada/product-list", timeout=45000)
            await page.wait_for_timeout(10000)
            
            token = await page.evaluate("localStorage.getItem('_token')")
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            
            print("Fetching categories...")
            cat_response = await page.request.get("https://api.kingfood.co/v1/categories/fulldata", headers=headers)
            categories_tree = await cat_response.json()
            
            all_flat = flatten_categories(categories_tree)
            print(f"Flattened total categories: {len(all_flat)}")
            
            target_names = ["2.EGGS", "2.DELICA", "2.VEGETABLES", "2.BAKERY", "2.FRUITS"]
            matched = []
            for item in all_flat:
                name = str(item.get("name", "")).strip()
                if name in target_names:
                    matched.append(item)
                    print(f"Matched Category: '{name}' -> ID: {item.get('id')}")
                    
            print(f"Matched {len(matched)} of {len(target_names)} categories.")
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
