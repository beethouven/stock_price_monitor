from ui_scraper import TSEStockPage, create_chrome_driver
from config import load_data_file
from PIL import Image
import os


stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']


def test_get_stock_price():
    driver = create_chrome_driver()
    page = TSEStockPage(driver)

    page.open(stock_number)
    price = page.get_price()

    assert price is not None
    os.makedirs("reports", exist_ok=True)  # 如果資料夾不存在就自動建立
    driver.save_screenshot("reports/ui_screenshot.png")

    img = Image.open("reports/ui_screenshot.png")
    img.thumbnail((600, 400))  # 等比例縮小
    img.convert("RGB").save("reports/ui_screenshot.jpg", format="JPEG", quality=80)

    driver.quit()



    driver.quit()
    