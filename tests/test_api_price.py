from api_client import get_price_from_api
from config import load_data_file

stock_list = load_data_file("test_targets.json")
stock_number = stock_list[0]['symbol']

# 取出全部的數字
# stock_number_list = [d['symbol'] for d in stock_list]
# print(stock_number_list)


def test_get_price_from_api():
    price = get_price_from_api(stock_number)

    # 驗證價錢不是 None
    assert price is not None, "回傳為 None，可能是 API 無資料或格式錯誤"

    # 驗證價錢為數字類型
    assert isinstance(price, (int, float)), f"回傳型態錯誤：{type(price)}"

    # 驗證價錢大於 0（合理性判斷）
    assert price > 0, f"價格異常：{price}"