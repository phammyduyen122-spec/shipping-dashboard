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
        
        # Monitor API requests
        requests_log = []
        
        async def handle_response(response):
            url = response.url
            if "kingfood.co" in url and any(kw in url.lower() for kw in ["api", "graphql", "query", "product", "list", "filter"]):
                status = response.status
                try:
                    # Only print headers or small metadata to avoid huge print
                    headers = response.headers
                    content_type = headers.get("content-type", "")
                    if "json" in content_type:
                        try:
                            res_json = await response.json()
                            requests_log.append((url, status, "JSON", list(res_json.keys()) if isinstance(res_json, dict) else "list"))
                        except:
                            requests_log.append((url, status, "JSON_FAILED", None))
                    else:
                        requests_log.append((url, status, "OTHER", None))
                except Exception as e:
                    pass

        page.on("response", handle_response)
        
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
            await page.wait_for_timeout(10000)
            
            print("Opening filter...")
            filter_button = page.locator("button .anticon-filter, button:has(svg), .anticon-filter").first
            await filter_button.click()
            await page.wait_for_timeout(2000)
            
            print("Opening 'Danh mục' tree select...")
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            await target_form_item.locator(".ant-select-selector").first.click(force=True)
            await page.wait_for_timeout(2000)
            
            # Click switchers
            switcher_bakery = page.locator(".ant-select-tree-treenode:has-text('1.BAKERY AND DELICA') .ant-select-tree-switcher").first
            if await switcher_bakery.count() > 0:
                await switcher_bakery.click(force=True)
            switcher_fresh = page.locator(".ant-select-tree-treenode:has-text('1.FRESH FOOD') .ant-select-tree-switcher").first
            if await switcher_fresh.count() > 0:
                await switcher_fresh.click(force=True)
            await page.wait_for_timeout(2000)
                
            list_holder = page.locator(".ant-select-tree-list-holder").first
            target_cats = ["2.BAKERY", "2.DELICA", "2.EGGS", "2.FRUITS", "2.VEGETABLES"]
            
            for cat in target_cats:
                for scroll_top in range(0, 800, 50):
                    await list_holder.evaluate(f"el => el.scrollTop = {scroll_top}")
                    await page.wait_for_timeout(100)
                    cat_elem = page.locator(f".ant-select-tree-treenode:has-text('{cat}') .ant-select-tree-node-content-wrapper").first
                    if await cat_elem.count() > 0 and await cat_elem.is_visible():
                        await cat_elem.click(force=True)
                        await page.wait_for_timeout(200)
                        break
                        
            print("Clicking 'Áp dụng' button...")
            submit_btn = page.locator(".ant-drawer-content button:has-text('Áp dụng')").first
            await submit_btn.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)
            
            print("\nAPI requests intercepted:")
            for url, status, rtype, keys in requests_log:
                print(f"URL: {url[:100]}")
                print(f"  Status: {status}, Type: {rtype}, Keys: {keys}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
