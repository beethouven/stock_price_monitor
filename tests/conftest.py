import sys
from pathlib import Path
import pytest
import os
import base64
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

def embed_base64_image(path, width=600):
    if not os.path.exists(path):
        print(f"⚠️ 圖片不存在：{path}")
        return ""
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            ext = os.path.splitext(path)[1][1:]
            return f'<img src="data:image/{ext};base64,{encoded}" width="{width}"/>'
    except Exception as e:
        print("❌ 編碼失敗：", e)
        return ""

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and "test_ui.py" in item.location[0]:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H")
        folder = f"reports/{timestamp}/photo/"

        if os.path.exists(folder) and pytest_html:
            for filename in os.listdir(folder):
                if filename.lower().endswith(".jpg"):
                    full_path = os.path.join(folder, filename)
                    html_img = embed_base64_image(full_path, width=600)
                    if html_img:
                        extra.append(pytest_html.extras.html(html_img))

    report.extra = extra