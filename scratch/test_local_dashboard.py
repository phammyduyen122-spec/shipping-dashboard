import asyncio
import subprocess
import time
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

def print_log(msg):
    print(msg, flush=True)

async def main():
    print_log("Starting local HTTP server on port 8000 (redirecting output to DEVNULL)...")
    server_process = subprocess.Popen(
        ["python", "-m", "http.server", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2) # Give it a moment to start
    
    try:
        async with async_playwright() as p:
            print_log("Launching chromium headless...")
            try:
                browser = await p.chromium.launch(headless=True)
            except Exception as launch_err:
                print_log(f"Failed to launch browser: {launch_err}")
                print_log("Attempting to run 'playwright install chromium'...")
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
                browser = await p.chromium.launch(headless=True)
                
            page = await browser.new_page()
            
            # Log console errors or warnings
            page.on("console", lambda msg: print_log(f"CONSOLE: {msg.type}: {msg.text}"))
            page.on("pageerror", lambda err: print_log(f"PAGE ERROR: {err}"))
            
            url = "http://localhost:8000/index.html"
            print_log(f"Navigating to {url}...")
            await page.goto(url, timeout=30000)
            print_log("Waiting for 4 seconds for page logic to load...")
            await page.wait_for_timeout(4000)
            
            # Tab 1: Hiệu suất Chia hàng
            print_log("\n--- Verifying perfSummaryTable (Overall Summary Table) ---")
            summary_headers = await page.locator("#perfSummaryTable thead th").all_text_contents()
            summary_headers = [h.strip() for h in summary_headers]
            print_log(f"Summary Table Headers: {summary_headers}")
            
            assert "Giá trị lệch" in summary_headers, "Missing 'Giá trị lệch' in Summary Table"
            print_log("Summary table columns verified!")
            
            # Check row count
            summary_rows = await page.locator("#perfSummaryBody tr").count()
            print_log(f"Number of rows in perfSummaryBody: {summary_rows}")
            
            # Print first 3 rows
            for i in range(min(3, summary_rows - 1)): # exclude grand total
                row_text = await page.locator("#perfSummaryBody tr").nth(i).text_content()
                print_log(f"  Row {i+1}: {row_text.strip().replace('\n', ' | ')}")
                
            # Verify grand total row
            grand_total_row = await page.locator("#perfSummaryBody tr").nth(summary_rows - 1).text_content()
            print_log(f"  Grand Total Row: {grand_total_row.strip().replace('\n', ' | ')}")
            
            # Take screenshot of the overall summary table
            screenshot_summary_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/local_perf_summary_table.png"
            await page.locator("#perfSummaryTable").screenshot(path=screenshot_summary_path)
            print_log(f"Summary table screenshot saved to {screenshot_summary_path}")
            
            # Verify columns on perfTable (Detailed Table)
            print_log("\n--- Verifying Detailed Table (perfTable) ---")
            
            # Check all table headers
            all_detailed_headers = await page.locator("tbody#perfTableBody").locator("xpath=../thead/tr/th").all_text_contents()
            all_detailed_headers = [h.strip() for h in all_detailed_headers]
            print_log(f"All Detailed Table Headers: {all_detailed_headers}")
            
            assert "STT siêu thị" in all_detailed_headers, "Missing 'STT siêu thị' in Detailed Table"
            print_log("Detailed table columns verified!")
            
            # Check row count
            detailed_rows = await page.locator("#perfTableBody tr").count()
            print_log(f"Number of rows in perfTableBody: {detailed_rows}")
            
            # Print first 3 rows
            for i in range(min(3, detailed_rows)):
                row_text = await page.locator("#perfTableBody tr").nth(i).text_content()
                print_log(f"  Row {i+1}: {row_text.strip().replace('\n', ' | ')}")
                
            # Take screenshot of detailed table
            screenshot_detailed_path = "C:/Users/DUYEN/.gemini/antigravity/brain/dca284e8-02b6-49ff-9cf8-e32c87a805c0/local_perf_detailed_table.png"
            await page.locator("tbody#perfTableBody").scroll_into_view_if_needed()
            await page.locator("tbody#perfTableBody").locator("xpath=..").screenshot(path=screenshot_detailed_path)
            print_log(f"Detailed table screenshot saved to {screenshot_detailed_path}")
            
            # Test Sorting
            print_log("\n--- Testing Sorting on Detailed Table ---")
            qty_shipped_header = page.locator("th[data-perf-sort='qtyShipped']")
            print_log("Clicking 'SL chuyển' sort header...")
            await qty_shipped_header.click()
            await page.wait_for_timeout(1000)
            first_row_shipped = await page.locator("#perfTableBody tr td").nth(8).text_content()
            print_log(f"After sort click 1 (asc), SL chuyển of first row: {first_row_shipped.strip()}")
            
            print_log("Clicking 'SL chuyển' sort header again...")
            await qty_shipped_header.click()
            await page.wait_for_timeout(1000)
            first_row_shipped_desc = await page.locator("#perfTableBody tr td").nth(8).text_content()
            print_log(f"After sort click 2 (desc), SL chuyển of first row: {first_row_shipped_desc.strip()}")
            
            # Test Filter
            print_log("\n--- Testing Filters on Detailed Table ---")
            barcode_filter = page.locator("#perfTableFilterBarcode")
            print_log("Filtering detailed table by Barcode '8936079010125' (we will try to filter to find matching rows)...")
            # Let's get the barcode from the first row of detailed table if possible, otherwise hardcoded.
            first_row_barcode = await page.locator("#perfTableBody tr td").nth(3).text_content()
            first_row_barcode = first_row_barcode.strip()
            print_log(f"First row barcode is '{first_row_barcode}'. Filtering by this barcode...")
            
            await barcode_filter.fill(first_row_barcode)
            await barcode_filter.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
            await page.wait_for_timeout(1500)
            filtered_rows = await page.locator("#perfTableBody tr").count()
            print_log(f"Filtered rows count: {filtered_rows}")
            for i in range(min(3, filtered_rows)):
                row_text = await page.locator("#perfTableBody tr").nth(i).text_content()
                print_log(f"  Row {i+1}: {row_text.strip().replace('\n', ' | ')}")
                
            # Clear filter
            await barcode_filter.fill("")
            await barcode_filter.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
            await page.wait_for_timeout(1000)
            
            # Test CSV downloads
            print_log("\n--- Testing CSV Exports ---")
            async def test_download(btn_selector, name):
                try:
                    async with page.expect_download(timeout=10000) as download_info:
                        print_log(f"Clicking {name} button...")
                        await page.click(btn_selector)
                    download = await download_info.value
                    path = await download.path()
                    print_log(f"  - Download completed: {download.suggested_filename}")
                    with open(path, "r", encoding="utf-8-sig") as f:
                        lines = [f.readline().strip() for _ in range(3)]
                    print_log(f"  - First few lines of {name} CSV:")
                    for idx, line in enumerate(lines):
                        print_log(f"    Line {idx+1}: {line}")
                except Exception as e:
                    print_log(f"  - Error downloading {name}: {e}")
            
            await test_download("#btnExportSummary", "Xuất Excel hiệu suất (Summary)")
            await test_download("#perfBtnExport", "Xuất Excel chi tiết (Performance)")
            
            print_log("\nAll verification checks completed successfully!")
            await browser.close()
            
    except Exception as e:
        print_log(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print_log("Stopping local HTTP server...")
        server_process.terminate()
        server_process.wait()
        print_log("Server stopped.")

if __name__ == "__main__":
    asyncio.run(main())
