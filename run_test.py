import argparse
import os
import pytest
from datetime import datetime

def create_report_folder(folder="reports"):
    os.makedirs(folder, exist_ok=True)

def get_timestamp_hour():
    return datetime.now().strftime("%Y-%m-%d_%H")  # 精確到小時

def build_pytest_command(args):
    # 建立報表資料夾
    create_report_folder()

    # 檔案命名 ➝ 保留使用者自訂，否則加時間戳
    timestamp = get_timestamp_hour()
    report_file = args.report or f"reports/test_report_{timestamp}.html"

    # 建立 pytest 參數 list
    pytest_args = [
        "--html=" + report_file,
        "--self-contained-html"
    ]

    if args.target:
        pytest_args += args.target
    else:
        pytest_args.append("tests/")  # 預設執行 tests 資料夾

    if args.kword:
        pytest_args += ["-k", args.kword]

    if args.marker:
        pytest_args += ["-m", args.marker]

    return pytest_args, report_file

def main():
    parser = argparse.ArgumentParser(description="執行 pytest 並產出 HTML 報表（自動嵌入截圖）")
    parser.add_argument("--target", nargs="+", help="指定測試檔案或函式，例如 test_login.py::test_login")
    parser.add_argument("--kword", help="使用 -k 關鍵字模糊搜尋測試函式，例如 'login and success'")
    parser.add_argument("--marker", help="使用 -m 執行被特定 @pytest.mark 標記的測試，如 smoke、regression")
    parser.add_argument("--report", help="自訂報表名稱，預設為 reports/test_report_時間戳.html")
    args = parser.parse_args()

    pytest_args, report_path = build_pytest_command(args)

    print("⏳ 執行 pytest 測試中...")
    print("📁 測試目標：", args.target or "tests/")
    print("🔎 關鍵字 -k：", args.kword or "(無)")
    print("🏷️ 標籤 -m：", args.marker or "(無)")
    print("📄 報表輸出：", report_path)

    exit_code = pytest.main(pytest_args)
    print(f"✅ 測試完成！（Exit Code: {exit_code}）報表已產出 🎉")

if __name__ == "__main__":
    main()