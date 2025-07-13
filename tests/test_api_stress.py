from api_stress import run_stress_test, send_request, assert_stress_case
from config import load_data_file
from data_record import write_json
from datetime import datetime

def test_api_stress():
    stock_list = load_data_file("test_targets.json")
    stock_number = stock_list[0]['symbol']
    date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id={stock_number}&start_date={date}"
    
    config = load_data_file("load_test_config.json")
    threads = config.get("threads", 5)
    requests_per_thread = config.get("requests_per_thread", 5)
    duration_limit = config.get("duration_limit", 1)

    request_func = lambda: send_request(url)
    response = run_stress_test(threads, requests_per_thread, request_func)

    error_log = []
    for idx, item in enumerate(response):
        result = assert_stress_case(idx, item, duration_limit)
        error_log.extend(result)

    if error_log:
        write_json(error_log, "log/error_report.jsonl")