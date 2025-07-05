from ui_scraper import TSEStockPage, create_chrome_driver
from config import load_data_file
from PIL import Image
import os
from datetime import datetime

stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']



def save_ui_screenshot(driver, test_name):
    # 建立 UI 測試資料夾
    folder = "reports/ui_test"
    os.makedirs(folder, exist_ok=True)

    # 小時級時間戳命名
    timestamp = datetime.now().strftime("%Y%m%d_%H")
    base_name = f"{test_name}_{timestamp}"
    png_path = os.path.join(folder, base_name + ".png")
    jpg_path = os.path.join(folder, base_name + ".jpg")

    # Selenium 儲存初始 PNG 截圖
    driver.save_screenshot(png_path)

    # 使用 Pillow 處理圖片（縮圖 + 轉 JPEG）
    try:
        img = Image.open(png_path)
        img.thumbnail((600, 400))  # ✅ 等比例縮小至最大寬高
        img.convert("RGB").save(jpg_path, format="JPEG", quality=80)
    except Exception as e:
        print(f"❌ 圖片處理失敗：{e}")
        return None

    return jpg_path  # ✅ 最終輸出的 JPG 路徑（可嵌入報告）

def test_get_stock_price():
    driver = create_chrome_driver()
    try:
        page = TSEStockPage(driver)
        page.open(stock_number)
        price = page.get_price()

        assert price is not None
        save_ui_screenshot(driver, "test_get_stock_price")
        print(f"✅ 成功取得 {stock_number} 的股價：{price}")
    finally:
        driver.quit()
    