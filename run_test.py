import argparse
import os
import pytest
from datetime import datetime
import re

def create_report_folder(folder="reports"):
    os.makedirs(folder, exist_ok=True)

def get_timestamp_hour():
    return datetime.now().strftime("%Y-%m-%d_%H")  # 精確到小時

def build_pytest_command(args):
    create_report_folder()
    timestamp = get_timestamp_hour()
    timestamp_folder = f"reports/{timestamp}"
    os.makedirs(timestamp_folder, exist_ok=True)
    report_file = args.report or os.path.join(timestamp_folder, "report.html")

    pytest_args = [
        "--html=" + report_file,
        "--self-contained-html"
    ]

    if args.target:
        pytest_args += args.target
    else:
        pytest_args.append("tests/")

    if args.kword:
        pytest_args += ["-k", args.kword]

    if args.marker:
        pytest_args += ["-m", args.marker]

    return pytest_args, report_file

def verify_image_embedded(report_path):
    if not os.path.exists(report_path):
        print("❌ 報告檔案不存在，無法檢查圖片嵌入狀態")
        return
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            match = re.search(r'<img[^>]+src="([^"]+)"', html_content)
            if match:
                img_src = match.group(1)
                if img_src.startswith("data:image"):
                    print("✔️ 圖片已嵌入報告（Base64 形式）")
                else:
                    print("⚠️ 圖片仍為外連形式，請確認 --self-contained-html 是否生效")
                    print(f"🔗 圖片引用路徑：{img_src}")
            else:
                print("❗ 報告中未找到 <img> 標籤，可能未附圖")
    except Exception as e:
        print(f"❌ 檢查嵌入失敗：{e}")

def main():
    parser = argparse.ArgumentParser(description="執行 pytest 並產出 HTML 報表（自動嵌入截圖）")
    parser.add_argument("--target", nargs="+", help="指定測試檔案或函式")
    parser.add_argument("--kword", help="使用 -k 關鍵字模糊搜尋")
    parser.add_argument("--marker", help="使用 -m 執行被特定標記的測試")
    parser.add_argument("--report", help="自訂報表名稱，預設為 reports/test_report_時間戳.html")
    args = parser.parse_args()

    pytest_args, report_path = build_pytest_command(args)

    print("⏳ 執行 pytest 測試中...")
    print("📁 測試目標：", args.target or "tests/")
    print("🔎 關鍵字 -k：", args.kword or "(無)")
    print("🏷️ 標籤 -m：", args.marker or "(無)")
    print("📄 報表輸出：", report_path)

    exit_code = pytest.main(pytest_args)
    print(f"\n✅ 測試完成！（Exit Code: {exit_code}）")

    print("\n🔍 正在檢查圖片嵌入狀態...")
    verify_image_embedded(report_path)

if __name__ == "__main__":
    main()