import requests
def GetData(brand, date_from, date_to, api_key, limit):
    params = {
        'access_key': api_key,
        'date_from': date_from,
        'date_to': date_to,
        'limit' : 
    }
    api_result = requests.get(f"https://api.marketstack.com/v1/tickers/{brand}/eod")
    return ap