import requests
from urllib.parse import urlparse, unquote


def get_item_price(appid, market_hash_name):
    url = f"https://steamcommunity.com/market/priceoverview/?appid={appid}&currency=5&market_hash_name={market_hash_name}"
    response = requests.get(url)
    data = response.json()
    if isinstance(data, dict) and data['success']:
        price = data['lowest_price']
        price = price.replace(' pуб.', '').replace(',', '.')
        return float(price)


def extract_appid_and_market_hash_name(url):
    parsed_url = urlparse(url)
    appid, market_hash_name = parsed_url.path.split('/')[3:5]
    return appid, unquote(market_hash_name)


url = "https://steamcommunity.com/market/listings/570/Bracers%20of%20Forlorn%20Precipice"
appid, market_hash_name = extract_appid_and_market_hash_name(url)

print(get_item_price(appid, market_hash_name))
