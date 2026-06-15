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
            if not token:
                print("❌ ERROR: Could not find JWT token in localStorage!")
                return
                
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Fetch category metadata
            print("Fetching all categories metadata using token...")
            cat_response = await page.request.get(
                "https://api.kingfood.co/v1/categories/fulldata",
                headers=headers
            )
            if cat_response.status != 200:
                print(f"Failed to fetch categories: {cat_response.status}")
                return
                
            categories_tree = await cat_response.json()
            all_flat = flatten_categories(categories_tree)
            print(f"Flattened total categories: {len(all_flat)}")
            
            # Target categories
            target_names = ["2.EGGS", "2.DELICA", "2.VEGETABLES", "2.BAKERY", "2.FRUITS"]
            target_cats = []
            
            for item in all_flat:
                name = str(item.get("name", "")).strip()
                if name in target_names:
                    target_cats.append(item)
                    print(f"Matched Category: '{name}' -> ID: {item.get('id')}")
            
            target_ids = [c.get("id") for c in target_cats]
            print(f"Target category IDs: {target_ids}")
            
            # Query variants
            payload = {
                "sort_by": "created_at",
                "sort_type": -1,
                "skip": 0,
                "limit": 10000,
                "deleted": False,
                "category_ids": target_ids,
                "created_by": [],
                "updated_by": []
            }
            
            print("Querying variants list from v2/variants/getList using token...")
            var_response = await page.request.post(
                "https://api.kingfood.co/v2/variants/getList",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if var_response.status != 200:
                print(f"Failed to fetch variants list: {var_response.status}")
                print(await var_response.text())
                return
                
            var_data = await var_response.json()
            items = var_data.get("items", [])
            total = var_data.get("total", 0)
            print(f"API returned {len(items)} items (total in database: {total})")
            
            mapping = {}
            for item in items:
                barcode = item.get("barcode", "").strip()
                item_code = item.get("variant_code", "").strip() or item.get("internal_code", "").strip()
                cat_path = item.get("category_path_name", "")
                
                matched_category = ""
                for target_name in target_names:
                    if target_name in cat_path:
                        matched_category = target_name
                        break
                        
                if not matched_category:
                    cat_id = item.get("category_id")
                    for tc in target_cats:
                        if tc.get("id") == cat_id:
                            matched_category = tc.get("name")
                            break
                            
                entry = {
                    "itemName": item.get("name", ""),
                    "category": matched_category,
                    "categoryPath": cat_path,
                    "unit": item.get("description", "") or "CÁI"
                }
                
                if barcode:
                    mapping[barcode] = entry
                if item_code:
                    mapping[item_code] = entry
                    
            print(f"Built mapping database with {len(mapping)} keys.")
            
            # Save mapping to json
            with open("scratch/category_mapping.json", "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=2)
            print("Successfully saved mapping to scratch/category_mapping.json")
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
