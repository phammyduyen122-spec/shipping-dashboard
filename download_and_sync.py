import os
import sys
import asyncio
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import subprocess

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Calculate dates for the last 3 days based on Vietnam Time (ICT, UTC+7)
    from datetime import timezone
    now_utc = datetime.now(timezone.utc)
    now_ict = now_utc + timedelta(hours=7)
    dates = []
    for i in range(3):
        d = now_ict - timedelta(days=i)
        dates.append((d.strftime("%d/%m/%Y"), d.strftime("%Y-%m-%d")))
        
    print(f"--- START AUTOMATIC DOWNLOAD FOR THE LAST 7 DAYS ---")
    
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        # 1. Download DS phiếu chuyển from next.kingfood.co
        print("\n--- 1. DOWNLOADING FROM next.kingfood.co ---")
        try:
            print("Logging into next.kingfood.co...")
            await page.goto("https://next.kingfood.co/", timeout=45000)
            await page.wait_for_timeout(2000)
            
            await page.fill("#normal_login_account", "SC015807")
            await page.fill("#normal_login_password", "Yuanxxinh@1202")
            await page.click("button[type='submit']")
            
            print("Waiting for dashboard loading...")
            await page.wait_for_timeout(15000)
            
            print("Navigating to transfer item list...")
            await page.goto("https://next.kingfood.co/operation/transfer-item/transfer-item-list")
            await page.wait_for_timeout(8000)
            
            from_date_xpath = "//div[contains(@class, 'ant-form-item')][.//*[text()='Ngày chuyển']]//input[@placeholder='Từ ngày']"
            to_date_xpath = "//div[contains(@class, 'ant-form-item')][.//*[text()='Ngày chuyển']]//input[@placeholder='Đến ngày']"
            
            for d_str, d_file in dates:
                print(f"\nProcessing date next.kingfood.co: {d_str}")
                try:
                    from_input = page.locator(from_date_xpath)
                    if not await from_input.is_visible():
                        print("Filter panel is closed. Opening it...")
                        await page.locator(".ant-input-affix-wrapper ~ button").first.click()
                        await page.wait_for_timeout(2000)
                    
                    await from_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(d_str)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)
                    
                    await page.locator(to_date_xpath).click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(d_str)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(1000)
                    
                    print("Applying filter...")
                    await page.locator("button:has-text('Áp dụng')").click()
                    await page.wait_for_timeout(5000)
                    
                    print("Opening export dropdown...")
                    await page.locator("button:has-text('Xuất file')").click()
                    await page.wait_for_timeout(1500)
                    
                    async def trigger_transfer_download():
                        await page.locator("text='Chi tiết phiếu chuyển theo filter'").click()
                    
                    print("Clicking export and expecting download...")
                    async with page.expect_download(timeout=120000) as download_info:
                        await trigger_transfer_download()
                    download = await download_info.value
                    target_path = f"transfer_{d_file}.xlsx"
                    await download.save_as(target_path)
                    print(f"Saved to {target_path}")
                except Exception as e:
                    print(f"Failed to download transfer for {d_str}: {e}")
                
        except Exception as e:
            print(f"Error downloading from next.kingfood.co: {e}")
            
        # 2. Download performance report from kdb.kingfood.co
        print("\n--- 2. DOWNLOADING FROM kdb.kingfood.co ---")
        try:
            print("Logging into kdb.kingfood.co...")
            await page.goto("https://kdb.kingfood.co/login", timeout=45000)
            await page.fill("input[name='account']", "SC015807")
            await page.fill("input[name='password']", "Yuanxxinh@1202")
            await page.click("button:has-text('ĐĂNG NHẬP')")
            await page.wait_for_timeout(5000)
            
            print("Navigating to transfers_transit_items...")
            await page.goto("https://kdb.kingfood.co/transfer-item/transfers_transit_items")
            
            print("Waiting for page elements to load...")
            await page.wait_for_selector("button.toggle-btn", timeout=30000)
            
            start_xpath = "//div[contains(@class, 'w-50') or contains(@class, 'p-1')][.//*[text()='Ngày chuyển mong muốn']]//input[@id='start-date-id']"
            end_xpath = "//div[contains(@class, 'w-50') or contains(@class, 'p-1')][.//*[text()='Ngày chuyển mong muốn']]//input[@id='end-date-id']"
            start_input = page.locator(start_xpath)
            end_input = page.locator(end_xpath)
            
            for d_str, d_file in dates:
                print(f"\nProcessing date kdb.kingfood.co: {d_str}")
                try:
                    if not await start_input.is_visible():
                        print("Filter panel is closed. Opening it...")
                        await page.locator("button.toggle-btn").first.click()
                        await page.wait_for_timeout(2000)
                    
                    await start_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(d_str)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)
                    
                    await end_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(d_str)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(1000)
                    
                    print("Applying filters (clicking Tìm kiếm)...")
                    await page.locator("text='Tìm kiếm'").first.click()
                    await page.wait_for_timeout(5000)
                    
                    print("Clicking 'Xuất file' dropdown...")
                    await page.locator("button:has-text('Xuất file')").click()
                    await page.wait_for_timeout(1500)
                    
                    async def trigger_perf_download():
                        await page.locator("text='Chi tiết yêu cầu'").click()
                        
                    print("Clicking export and expecting download...")
                    async with page.expect_download(timeout=120000) as download_info:
                        await trigger_perf_download()
                    download = await download_info.value
                    perf_dir = "performance dashboard"
                    os.makedirs(perf_dir, exist_ok=True)
                    target_path = os.path.join(perf_dir, f"chi-tiet-chia-qua-canh_{d_file}.xlsx")
                    await download.save_as(target_path)
                    print(f"Saved to {target_path}")
                except Exception as e:
                    print(f"Failed to download performance for {d_str}: {e}")
                    
        except Exception as e:
            print(f"Error downloading from kdb.kingfood.co: {e}")
            
        await browser.close()
        
        # 3. Trigger parse_excel.py
        print("\n--- 3. RUNNING PARSER ---")
        result = subprocess.run([sys.executable, "parse_excel.py"], capture_output=True, text=True, encoding="utf-8")
        print("Parser output:")
        print(result.stdout)
        if result.returncode == 0:
            print("🎉 SUCCESS: Data synced successfully!")
        else:
            print("❌ ERROR: Parser failed with error:")
            print(result.stderr)

if __name__ == "__main__":
    asyncio.run(main())
