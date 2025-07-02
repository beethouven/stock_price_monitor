from ui_scraper import TSEStockPage, create_chrome_driver
from config import load_data_file

stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']

# 取出全部的數字
# stock_number_list = [d['symbol'] for d in stock_list]
# print(stock_number_list)

def test_get_stock_price():
    driver = create_chrome_driver()
    page = TSEStockPage(driver)

    page.open(stock_number)
    price = page.get_price()

    assert price is not None
    driver.quit()
    