import requests
import time
from urllib3.exceptions import IncompleteRead

def get_item_listings(market_hash_name):
    url = f"https://steamcommunity.com/market/listings/730/{market_hash_name}/render/?query=&start=0&count=100&country=US&language=english&currency=1"
    response = requests.get(url)
    data = response.json()
    print(response)
    return data


# Пример использования:
market_hash_name = "AWP | Chrome Cannon (Field-Tested)"
listings = get_item_listings(market_hash_name)

def get_float_value(asset_id, cookies):
    while True:
        try:
            url = f"https://api.steampowered.com/IEconItems_730/GetAssetClassInfo/v0001/?appid=730&class_count=1&classid0={asset_id}"
            response = requests.get(url, cookies=cookies)
            data = response.json()
            float_value = data['result'][str(asset_id)]['descriptions'][4]['value']
            return float_value
        except IncompleteRead:
            continue

cookies = {"sessionid": "8887610a3121b5ca98f15c75", "steamLoginSecure": "76561198021972207%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEVDRV8yNDA4MTg4RF9CMEVFRCIsICJzdWIiOiAiNzY1NjExOTgwMjE5NzIyMDciLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MTQ2Mzg0NzksICJuYmYiOiAxNzA1OTExNjQzLCAiaWF0IjogMTcxNDU1MTY0MywgImp0aSI6ICIwRUY2XzI0NUIxMjA1XzI3QjBBIiwgIm9hdCI6IDE3MDkzMDg0NDUsICJydF9leHAiOiAxNzI3MzMxNTU5LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNjIuMjE3LjE4NC4xNzMiLCAiaXBfY29uZmlybWVyIjogIjYyLjIxNy4xODQuMTczIiB9.ebkn7CBQvq4Rd4Nd2BoOK7JgB-PJWX5ozh5lzFRLjY1T8e9Cm77071pRegz1aPxA6at3KaVj7qMZ2oDvI7aNDg	"}
for listing in listings['listinginfo'].values():
    asset_id = listing['asset']['id']
    print(get_float_value(asset_id, cookies))
    time.sleep(3)


# success
# start
# pagesize
# total_count
# results_html
# listinginfo
# assets
# currency
# hovers
# app_data