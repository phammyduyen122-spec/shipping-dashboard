import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        print("Launching browser to verify Category Table staff filter and status alignment...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, timeout=60000, wait_until="load")
            print("Loaded. Waiting for JS initialization...")
            await page.wait_for_timeout(10000)
            
            # Click Tab 2
            print("Switching to Tab 2...")
            await page.locator("#tabPerformanceReport").click(timeout=10000)
            await page.wait_for_timeout(3000)
            
            # 1. Verify Status Dropdown options in Tab 2
            print("Checking Tab 2 status filter checkboxes...")
            status_container = page.locator("#perfFilterStatusContainer")
            await status_container.locator(".multiselect-select").click(timeout=5000)
            await page.wait_for_timeout(1000)
            checkbox_options = await status_container.locator("input[type='checkbox']").all()
            print(f"Found {len(checkbox_options)} status options in Tab 2 filter:")
            for opt in checkbox_options:
                val = await opt.get_attribute("value")
                print(f"  - Status Value: {val}")
            await status_container.locator(".multiselect-select").click(timeout=5000)
            await page.wait_for_timeout(500)
            
            # 2. Check initial state of Category table
            title_text = await page.locator("#perfF1TableTitle").inner_text()
            header_text = await page.locator("#perfF1TableHeaderName").inner_text()
            print(f"Initial F1 Table Title: {title_text}")
            print(f"Initial F1 Table Header: {header_text}")
            initial_rows = await page.locator("#perfF1CategoryBody tr").all_inner_texts()
            print(f"Initial F1 Category Table Rows Count: {len(initial_rows)}")
            
            # 3. Test Local "Tìm nhân sự" input box on Category table
            print("\nTesting local 'Tìm nhân sự' search input...")
            user_search_input = page.locator("#perfF1UserSearch")
            await user_search_input.fill("001")
            await page.wait_for_timeout(2000)
            
            filtered_rows = await page.locator("#perfF1CategoryBody tr").all_inner_texts()
            print(f"Category Table Rows Count after typing '001': {len(filtered_rows)}")
            for idx, r in enumerate(filtered_rows):
                print(f"  Row {idx+1}: {r}")
                if "001" not in r:
                    errors.append(f"Category table row does not match search query '001': {r}")
            
            # Clear search
            print("Clearing local search...")
            await user_search_input.fill("")
            await page.wait_for_timeout(1000)
            
            # 4. Test Global "Nhóm nhân sự" Filter Dropdown
            print("\nOpening global Nhóm nhân sự dropdown...")
            group_container = page.locator("#perfFilterGroupContainer")
            await group_container.locator(".multiselect-select").click(timeout=5000)
            await page.wait_for_timeout(1000)
            
            # Check F2
            print("Checking F2 in global Nhóm nhân sự filter...")
            f2_checkbox = group_container.locator("input[type='checkbox'][value='F2']")
            await f2_checkbox.check()
            await page.wait_for_timeout(3000)
            
            # Verify F1 Category Table updated automatically
            title_text_f2 = await page.locator("#perfF1TableTitle").inner_text()
            header_text_f2 = await page.locator("#perfF1TableHeaderName").inner_text()
            print(f"F2 Table Title after global change: {title_text_f2}")
            print(f"F2 Table Header after global change: {header_text_f2}")
            f2_rows = await page.locator("#perfF1CategoryBody tr").all_inner_texts()
            print(f"F2 Category Table Rows Count: {len(f2_rows)}")
            
            # Verify Top 10 CTV rankings has F2 workers
            top10_ctv_names = await page.locator("#perfTopCTVBody tr td:nth-child(3)").all_inner_texts()
            print(f"Top 10 CTV workers visible: {top10_ctv_names}")
            for name in top10_ctv_names:
                if name != "Không rõ" and not name.lower().startswith("f2"):
                    errors.append(f"Top 10 CTV table contains non-F2 worker: {name}")

            # Close dropdown and take final screenshot
            await group_container.locator(".multiselect-select").click(timeout=5000)
            await page.wait_for_timeout(500)
            
            walkthrough_screenshot = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/final_aligned_screenshot.png"
            await page.screenshot(path=walkthrough_screenshot)
            print(f"Saved main walkthrough screenshot to {walkthrough_screenshot}")

        except Exception as e:
            print(f"Error occurred: {e}")
            errors.append(f"Error: {e}")
            
        await browser.close()
        
        if errors:
            print("\n❌ Verification Failed:")
            for err in errors:
                print(f"  {err}")
        else:
            print("\n🎉 SUCCESS: All verification steps passed perfectly with no errors!")

if __name__ == "__main__":
    asyncio.run(main())
