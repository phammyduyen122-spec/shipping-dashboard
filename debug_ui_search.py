import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))
        page.on("console", lambda msg: print(f"Browser Console {msg.type}: {msg.text}"))
        
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(3000)
        
        # Change dates
        await page.fill("#filterStartDate", "2026-06-08")
        await page.eval_on_selector("#filterStartDate", "el => el.dispatchEvent(new Event('change'))")
        await page.fill("#filterEndDate", "2026-06-09")
        await page.eval_on_selector("#filterEndDate", "el => el.dispatchEvent(new Event('change'))")
        await page.wait_for_timeout(1000)
        
        # Type yamazaky
        print("Typing yamazaky...")
        await page.fill("#filterItemCode", "yamazaky")
        await page.wait_for_timeout(2000)
        
        # Print dropdown inner HTML
        dropdown_html = await page.inner_html("#itemDropdownList")
        print("\n--- DROPDOWN INNER HTML ---")
        print(dropdown_html[:1000]) # first 1000 chars
        
        # Press Enter
        print("\nPressing Enter...")
        await page.locator("#filterItemCode").press("Enter")
        await page.wait_for_timeout(2000)
        
        # Print selected tags
        tags = await page.locator("#itemTagsContainer .tag-label").all_text_contents()
        print(f"Selected item tags in UI: {tags}")
        
        if errors:
            print("\n❌ Page Errors:")
            for err in errors:
                print(err)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
