from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


import platform

def create_chrome_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    try:
        service = Service(ChromeDriverManager().install())
        print("✅ 使用 webdriver-manager 成功安裝 driver")
    except Exception as e:
        print(f"⚠️ 下載失敗：{e} → 改用本地 driver")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        system = platform.system()
        if system == "Windows":
            local_driver_path = os.path.join(base_dir, "..", "drivers", "chromedriver.exe")
        elif system == "Linux":
            local_driver_path = os.path.join(base_dir, "..", "drivers", "chromedriver")  # 無副檔名
            os.chmod(local_driver_path, 0o755)  # 👈 加執行權限
        else:
            raise RuntimeError(f"不支援的作業系統：{system}")

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