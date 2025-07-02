==============================
🧪 Pytest 自動化測試執行腳本說明
==============================

檔案名稱：run_tests.py  
用途：執行 pytest 測試並自動產出 HTML 測試報表  
報表會輸出至 reports/ 資料夾中

------------------------------
✅ 基本用法
------------------------------

python run_tests.py

→ 執行 tests/ 資料夾下所有測試，並產出報表

------------------------------
🎯 指定測試目標
------------------------------

--target [檔案或函式]

範例：
python run_tests.py --target tests/test_login.py
python run_tests.py --target tests/test_api.py::TestOrder::test_invalid_input

可指定多個目標：
python run_tests.py --target tests/test_login.py tests/test_api.py

------------------------------
🔍 模糊比對測試名稱（-k）
------------------------------

--kword [關鍵字]

範例：
python run_tests.py --kword login
python run_tests.py --kword "login and fail"

------------------------------
🏷️ 指定測試標籤（-m）
------------------------------

--marker [標籤名稱]

範例：
python run_tests.py --marker smoke
python run_tests.py --marker "smoke and not regression"

需在測試中使用 @pytest.mark.smoke 等標記

------------------------------
📝 自訂報表名稱
------------------------------

--report [檔名.html]

範例：
python run_tests.py --report login_report.html

------------------------------
📦 綜合範例
------------------------------

python run_tests.py --target tests/test_api.py --kword login --marker smoke --report smoke_login.html

------------------------------
📁 預設目錄結構建議
------------------------------

your-project/
├── tests/                # 測試檔案放這裡
├── reports/              # 測試報表輸出資料夾
├── run_tests.py          # 執行腳本
└── requirements.txt      # 套件清單（需包含 pytest-html）

------------------------------
📦 套件需求
------------------------------

pip install pytest pytest-html