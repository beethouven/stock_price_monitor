from api_stress import run_stress_test, send_request
from config import load_data_file
from data_record import write_json
import re
import pytest_check as check
from datetime import datetime

stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']

send_request(stock_number)
error_log = []

def assert_stress_case(idx, data):
    if not isinstance(data, tuple):
        print(f"第{idx+1}筆請求資料格式有誤：{data}")
        return

    status, timing = data
    passed = re.fullmatch(r"\d{3}", str(status)) and timing < 0.3
    msg = None if passed else f"第{idx+1}筆請求有問題，狀態碼為 {status}，花費時間為 {timing:.4f} 秒"
    if not re.fullmatch(r"\d{3}", str(status)) or timing >= 0.3:
        error_log.append({
            "timestamp": datetime.now().isoformat(),
            "stock": stock_number,
            "response_status": status,
            "response_time": round(timing, 4),
            "reason": "狀態碼格式錯誤" if not re.fullmatch(r"\d{3}", str(status)) else ("時間超標" if timing >= 0.3 else "其他原因")
        })
    check.is_true(passed, msg)

def test_api_stress():
    response = run_stress_test()
    for idx, item in enumerate(response):
        assert_stress_case(idx, item)
    if len(error_log) > 0 :
        write_json(error_log, "log/error_report.jsonl")