import argparse
import subprocess
import os
from datetime import datetime

# 建立報表資料夾
os.makedirs("reports", exist_ok=True)

# 指令列參數
parser = argparse.ArgumentParser(description="執行 pytest 並產出 HTML 報表")
parser.add_argument(
    "--target", nargs="+", help="指定測試檔案或函式，例如 test_login.py::test_login"
)
parser.add_argument(
    "--kword", help="使用 -k 關鍵字模糊搜尋測試函式，例如 'login and success'"
)
parser.add_argument(
    "--marker", help="使用 -m 執行被特定 @pytest.mark 標記的測試，如 smoke、regression"
)
parser.add_argument(
    "--report", help="自訂報表名稱，預設為 reports/test_report_時間戳.html"
)

args = parser.parse_args()

# 組報表檔案名稱
report_file = args.report or f"reports/test_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"

# 組裝 pytest 指令
cmd = ["pytest", "--html=" + report_file, "--self-contained-html"]

if args.target:
    cmd += args.target
else:
    cmd.append("tests/")  # 預設跑整個 tests 資料夾

if args.kword:
    cmd += ["-k", args.kword]

if args.marker:
    cmd += ["-m", args.marker]

# 執行
print("⏳ 執行 pytest 測試中...")
print("📁 測試目標：", args.target or "tests/")
print("🔎 關鍵字 -k：", args.kword or "(無)")
print("🏷️ 標籤 -m：", args.marker or "(無)")
print("📄 報表輸出：", report_file)

subprocess.run(cmd)
print("✅ 測試完成！報表已產出 🎉")