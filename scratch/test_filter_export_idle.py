import asyncio
import os
import sys
from playwright.async_api import async_playwright
import pandas as pd

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
            
            print("Opening filter...")
            filter_button = page.locator("button .anticon-filter, button:has(svg), .anticon-filter").first
            await filter_button.click()
            await page.wait_for_timeout(3000)
            
            print("Opening 'Danh mục' tree select...")
            target_form_item = page.locator(".ant-form-item:has(label:has-text('Danh mục'))").first
            await target_form_item.locator(".ant-select-selector").first.click(force=True)
            await page.wait_for_timeout(3000)
            
            # Click switchers
            print("Clicking switchers...")
            switcher_bakery = page.locator(".ant-select-tree-treenode:has-text('1.BAKERY AND DELICA') .ant-select-tree-switcher").first
            if await switcher_bakery.count() > 0:
                await switcher_bakery.click(force=True)
                await page.wait_for_timeout(1000)
            switcher_fresh = page.locator(".ant-select-tree-treenode:has-text('1.FRESH FOOD') .ant-select-tree-switcher").first
            if await switcher_fresh.count() > 0:
                await switcher_fresh.click(force=True)
                await page.wait_for_timeout(1000)
                
            list_holder = page.locator(".ant-select-tree-list-holder").first
            target_cats = ["2.BAKERY", "2.DELICA", "2.EGGS", "2.FRUITS", "2.VEGETABLES"]
            
            for cat in target_cats:
                clicked = False
                for scroll_top in range(0, 800, 50):
                    await list_holder.evaluate(f"el => el.scrollTop = {scroll_top}")
                    await page.wait_for_timeout(150)
                    
                    cat_elem = page.locator(f".ant-select-tree-treenode:has-text('{cat}') .ant-select-tree-node-content-wrapper").first
                    if await cat_elem.count() > 0 and await cat_elem.is_visible():
                        await cat_elem.click(force=True)
                        await page.wait_for_timeout(300)
                        clicked = True
                        break
                print(f"Clicked {cat}: {clicked}")
                
            print("Clicking 'Áp dụng' button...")
            submit_btn = page.locator(".ant-drawer-content button:has-text('Áp dụng')").first
            await submit_btn.click()
            
            print("Waiting for network to become idle...")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000) # Additional safety margin
            
            # Print page body text to verify rows are visible in DOM
            body_text = await page.locator("body").inner_text()
            print("Verify if products exist in page text before export:")
            print("Contains 'TRỨNG GÀ':", "TRỨNG GÀ" in body_text)
            print("Contains 'TÁO':", "TÁO" in body_text)
            
            # Click "Xuất file"
            print("Clicking 'Xuất file' dropdown...")
            await page.click("button:has-text('Xuất file')")
            await page.wait_for_timeout(2000)
            
            print("Clicking option 'Sản phẩm thường - Thuộc tính SP'...")
            async with page.expect_download(timeout=180000) as download_info:
                await page.locator("text='Sản phẩm thường - Thuộc tính SP'").click()
            download = await download_info.value
            
            target_path = "filtered_attributes_idle.xlsx"
            await download.save_as(target_path)
            print(f"🎉 Downloaded filtered attributes to {target_path}")
            
            df = pd.read_excel(target_path)
            print(f"Number of rows imported: {len(df)}")
            print("Excel columns:")
            print(list(df.columns))
            print("First 5 rows preview:")
            print(df.head())
            
        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
