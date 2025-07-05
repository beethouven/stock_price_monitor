import requests
from datetime import datetime


def get_price_from_api(stock_id, date = datetime.now().strftime("%Y-%m-%d")):
    url = f'https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id={stock_id}&start_date={date}'
    response = requests.get(url)
    data = response.json()
    print(data)
    return float(data['data'][0]['close'])

