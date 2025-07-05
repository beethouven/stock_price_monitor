import sys
from pathlib import Path
import pytest
import os

# 專案根目錄/src 加入 sys.path
BASE_DIR = Path(__file__).resolve().parent.parent / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 捕捉測試報告
    outcome = yield
    report = outcome.get_result()

    # 只有在測試失敗或你想加入的階段加入附件
    
    extra = getattr(report, "extra", [])

    # 🖼️ 總是加圖檔，不限定失敗階段
    screenshot_path = "reports/ui_screenshot.png"
    if os.path.exists(screenshot_path):
        extra.append(pytest_html.extras.image(screenshot_path))

    report.extra = extra



def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')

