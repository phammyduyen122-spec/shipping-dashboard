import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(3000)
        
        # Change dates to 2026-06-08 to 2026-06-09
        print("Setting date range: 2026-06-08 to 2026-06-09...")
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(2000)
        
        # Select SP001222
        print("Searching and selecting SP001222...")
        await page.fill("#filterItemCode", "SP001222")
        await page.wait_for_timeout(1000)
        await page.click("#itemDropdownList span:has-text('SP001222')")
        await page.wait_for_timeout(500)
        await page.click("#btnConfirmSuggestions")
        await page.wait_for_timeout(2000)
        
        # Read SUMIFS card values for SP001222
        total_shipped = await page.inner_text("#sumifsTotalShipped")
        du_count = await page.inner_text("#sumifsDuCount")
        du_qty = await page.inner_text("#sumifsDuQty")
        thieu_count = await page.inner_text("#sumifsThieuCount")
        thieu_qty = await page.inner_text("#sumifsThieuQty")
        
        print("\n--- SUMIFS CARD VALUES FOR SP001222 ---")
        print(f"Total Shipped: {total_shipped}")
        print(f"Du Count: {du_count} | Qty: {du_qty}")
        print(f"Thieu Count: {thieu_count} | Qty: {thieu_qty}")
        
        # Clear filter
        await page.click("#clearFiltersBtn")
        await page.wait_for_timeout(1000)
        
        # Reset dates
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(1000)
        
        # Select SP001988
        print("\nSearching and selecting SP001988...")
        await page.fill("#filterItemCode", "SP001988")
        await page.wait_for_timeout(1000)
        await page.click("#itemDropdownList span:has-text('SP001988')")
        await page.wait_for_timeout(500)
        await page.click("#btnConfirmSuggestions")
        await page.wait_for_timeout(2000)
        
        # Read SUMIFS card values for SP001988
        total_shipped = await page.inner_text("#sumifsTotalShipped")
        du_count = await page.inner_text("#sumifsDuCount")
        du_qty = await page.inner_text("#sumifsDuQty")
        thieu_count = await page.inner_text("#sumifsThieuCount")
        thieu_qty = await page.inner_text("#sumifsThieuQty")
        
        print("\n--- SUMIFS CARD VALUES FOR SP001988 ---")
        print(f"Total Shipped: {total_shipped}")
        print(f"Du Count: {du_count} | Qty: {du_qty}")
        print(f"Thieu Count: {thieu_count} | Qty: {thieu_qty}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
