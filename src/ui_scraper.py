from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def create_chrome_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # 無頭模式，適合在伺服器上運行
    try:
        # 優先使用網路下載的 driver
        service = Service(ChromeDriverManager().install())
        print("✅ 使用 webdriver-manager 成功安裝 driver")
    except Exception as e:
        # 若被防火牆擋住就 fallback 使用相對路徑
        print(f"⚠️ 下載失敗：{e} → 改用本地 driver")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_driver_path = os.path.join(base_dir, "..", "drivers", "chromedriver.exe")
        service = Service(executable_path=local_driver_path)
    return webdriver.Chrome(service=service, options=options)


class TSEStockPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def open(self, symbol):
        url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
        self.driver.get(url)

    def get_price(self):
        return self.driver.find_element(By.XPATH, "//*[@id='main-0-QuoteHeader-Proxy']/div/div[2]/div[1]/div/span[1]").text