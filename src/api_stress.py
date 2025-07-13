import requests
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_fixed
import re
import pytest_check as check

# 重試機制：最多重試 3 次，每次間隔 2 秒
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_request(url):
    start = time.time()
    response = requests.get(url, timeout=3)
    duration = time.time() - start
    return response.status_code, duration

def run_stress_test(threads=10, requests_per_thread=5, request_func=None):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(request_func) 
            for _ in range(threads * requests_per_thread)
        ]
        for future in futures:
            status, duration = future.result()
            results.append((status, duration))
    return results

def assert_stress_case(idx, data, duration_limit=1):
    if not isinstance(data, tuple):
        print(f"第 {idx+1} 筆資料格式有誤：{data}")
        return []

    error_log = []
    status, timing = data
    passed = re.fullmatch(r"1\d{2}|2\d{2}", str(status)) and timing < duration_limit
    msg = None if passed else f"第 {idx+1} 筆請求失敗：狀態碼 {status}，花費 {timing:.4f} 秒"
    
    if not passed:
        error_log.append({
            "timestamp": datetime.now().isoformat(),
            "response_status": status,
            "response_time": round(timing, 4),
            "reason": "狀態碼錯誤" if not re.fullmatch(r"1\d{2}|2\d{2}", str(status)) 
                     else "超過時間門檻"
        })

    check.is_true(passed, msg)
    return error_log