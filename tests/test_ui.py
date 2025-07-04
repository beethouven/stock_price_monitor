from ui_scraper import TSEStockPage, create_chrome_driver
from config import load_data_file

stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']


def test_get_stock_price():
    driver = create_chrome_driver()
    page = TSEStockPage(driver)

    page.open(stock_number)
    price = page.get_price()

    assert price is not None
    driver.quit()
    