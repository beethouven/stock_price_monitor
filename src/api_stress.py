import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
from tenacity import retry, stop_after_attempt, wait_fixed

def send_request_with_retry(url):
    response = requests.get(url, timeout=3)  # 3秒沒回應就 timeout
    response.raise_for_status()
    return response


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_request(stock_id='2330', date = datetime.now().strftime("%Y-%m-%d")):
    url = f'https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id={stock_id}&start_date={date}'
    start = time.time()
    response = requests.get(url, timeout=3)
    duration = time.time() - start
    return response.status_code, duration

def run_stress_test(threads=10, requests_per_thread=5):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for _ in range(threads):
            for _ in range(requests_per_thread):
                futures.append(executor.submit(send_request))
        for future in futures:
            status, duration = future.result()
            results.append((status, duration))
    return results