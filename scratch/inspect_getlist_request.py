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
        
        captured_request = {}
        
        async def handle_request(request):
            url = request.url
            if "variants/getList" in url:
                captured_request["url"] = url
                captured_request["method"] = request.method
                captured_request["headers"] = request.headers
                captured_request["post_data"] = request.post_data
                print(f"Captured request: {url}")
                
        async def handle_response(response):
            url = response.url
            if "variants/getList" in url:
                try:
                    res_json = await response.json()
                    print(f"Captured response status: {response.status}")
                    print(f"Response items count: {len(res_json.get('items', [])) if isinstance(res_json, dict) else 'not a dict'}")
                    print(f"Response total: {res_json.get('total') if isinstance(res_json, dict) else 'none'}")
                    # Save a sample item
                    if isinstance(res_json, dict) and res_json.get('items'):
                        print("Sample item keys:", list(res_json['items'][0].keys()))
                        print("Sample item category/department:", {k: v for k, v in res_json['items'][0].items() if 'category' in k.lower() or 'department' in k.lower() or 'group' in k.lower()})
                except Exception as e:
                    print(f"Error reading response: {e}")

        page.on("request", handle_request)
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
            await page.wait_for_timeout(15000)
            
            print("Opening filter...")
            filter_button = page.locator("button .anticon-filter, button:has(svg), .anticon-filter").first
            await filter_button.click()
            await page.wait_for_timeout(2000)
            
            print("Opening 'Danh mục' tree select...")
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            await target_form_item.locator(".ant-select-selector").first.click(force=True)
            await page.wait_for_timeout(2000)
            
            # Click switcher for fresh food
            switcher_fresh = page.locator(".ant-select-tree-treenode:has-text('1.FRESH FOOD') .ant-select-tree-switcher").first
            if await switcher_fresh.count() > 0:
                await switcher_fresh.click(force=True)
                await page.wait_for_timeout(2000)
                
            list_holder = page.locator(".ant-select-tree-list-holder").first
            cat = "2.EGGS"
            clicked = False
            for scroll_top in range(0, 800, 50):
                await list_holder.evaluate(f"el => el.scrollTop = {scroll_top}")
                await page.wait_for_timeout(100)
                cat_elem = page.locator(f".ant-select-tree-treenode:has-text('{cat}') .ant-select-tree-node-content-wrapper").first
                if await cat_elem.count() > 0 and await cat_elem.is_visible():
                    await cat_elem.click(force=True)
                    await page.wait_for_timeout(200)
                    clicked = True
                    break
                    
            if clicked:
                print("Clicking 'Áp dụng' button...")
                submit_btn = page.locator(".ant-drawer-content button:has-text('Áp dụng')").first
                await submit_btn.click()
                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(5000)
                
                # Print captured request details
                if captured_request:
                    print("\nCaptured Request Details:")
                    print(f"Method: {captured_request['method']}")
                    print("Headers (Authorization):", captured_request['headers'].get('authorization', 'none'))
                    print("Post Data:")
                    try:
                        post_json = json.loads(captured_request['post_data'])
                        print(json.dumps(post_json, indent=2))
                    except:
                        print(captured_request['post_data'])
                else:
                    print("No variants/getList request captured!")
            else:
                print("Failed to click category '2.EGGS'")
                
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
