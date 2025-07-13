from PIL import Image
import os
from datetime import datetime
from selenium.webdriver.common.by import By

#建立測試資料夾 命名規則為 test_name_時間戳.png
# 並將圖片轉成等比例縮小的 JPG 格式，並設定品質
def save_ui_screenshot(driver, test_name, target_xpath=None, folder="reports/"+datetime.now().strftime("%Y-%m-%d_%H")+"/photo/", max_size=(800, 2000), quality=80):
    # 建立 UI 測試資料夾
    
    os.makedirs(folder, exist_ok=True)

    # 小時級時間戳命名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H")
    base_name = f"{test_name}_{timestamp}"

    if target_xpath:
        try:
            element = driver.find_element(By.XPATH, target_xpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            png_path = os.path.join(folder, base_name + "_element.png")
            element.screenshot(png_path)
        except Exception as e:
            print(f"❌ 元件截圖失敗：{e}")
            return None
    else:
        png_path = os.path.join(folder, base_name + ".png")
        driver.save_screenshot(png_path)

    jpg_path = os.path.join(folder, base_name + ".jpg")

    # 使用 Pillow 處理圖片（縮圖 + 轉 JPEG）
    try:
        img = Image.open(png_path)
        img.thumbnail(max_size)  # ✅ 等比例縮小至最大寬高
        img.convert("RGB").save(jpg_path, format="JPEG", quality=quality)
    except Exception as e:
        print(f"❌ 圖片處理失敗：{e}")
        return None

    return jpg_path  # ✅ 最終輸出的 JPG 路徑（可嵌入報告）