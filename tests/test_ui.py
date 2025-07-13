from ui_scraper import create_chrome_driver, open_page, get_element_text
from photo_management import save_ui_screenshot
from config import load_data_file

# 載入所有測試個案設定
test_cases = load_data_file("test_targets.json")

def test_all_ui_tasks():
    for case in test_cases:
        name = case["name"]
        symbol = case["symbol"]
        url = case["url"]
        xpath = case["components"][0]["xpath"]

        print(f"🚀 開始執行測試：{name}")

        driver = create_chrome_driver()
        try:
            open_page(driver, url)
            text = get_element_text(driver, xpath)

            assert text is not None
            save_ui_screenshot(driver, f"ui_{symbol}")
            # xpath = "//*[@id='main-0-QuoteHeader-Proxy']/div/div[1]/div/h1"
            save_ui_screenshot(driver, f"ui_{symbol}_element", target_xpath=xpath)
            print(f"✅ 成功取得 {symbol} 的資料：{text}")
        except Exception as e:
            print(f"❌ 測試失敗：{name} → {e}")
        finally:
            driver.quit()