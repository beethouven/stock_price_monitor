import requests

def get_price_from_api(url):
    response = requests.get(url)
    data = response.json()
    print(data)
    return float(data['data'][0]['close'])

