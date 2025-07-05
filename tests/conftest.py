import sys
from pathlib import Path
import pytest
import os
import base64
from datetime import datetime

# 專案根目錄/src 加入 sys.path
BASE_DIR = Path(__file__).resolve().parent.parent / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ✅ pytest-html plugin 存為全域變數
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")



# ✅ 將圖片轉成 base64 並產生 HTML <img> 標籤
def embed_base64_image(path, width=600):
    if not os.path.exists(path):
        print(f"⚠️ 圖片不存在：{path}")
        return ""
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            ext = os.path.splitext(path)[1][1:]  # 取得副檔名如 jpg、png
            return f'<img src="data:image/{ext};base64,{encoded}" width="{width}"/>'
    except Exception as e:
        print("❌ 編碼失敗：", e)
        return ""

# ✅ 測試完成後自動加圖片進報告（嵌入形式）
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        if "test_ui.py" in item.location[0]:                    
            folder = "reports/ui_test"
            # 小時級時間戳命名
            timestamp = datetime.now().strftime("%Y%m%d_%H")
            base_name = f"{item.name}_{timestamp}"
            jpg_path = os.path.join(folder, base_name + ".jpg")
            # ✅ 指定截圖路徑
            screenshot_path = jpg_path

            if os.path.exists(screenshot_path) and pytest_html:
                html_img = embed_base64_image(screenshot_path, width=600)
                if html_img:
                    extra.append(pytest_html.extras.html(html_img))

        report.extra = extra







