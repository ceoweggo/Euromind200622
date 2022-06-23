import requests
import os, json
import pandas as pd
from app.model import ProcessData
from config import Config
import model

dirname = os.path.dirname(__file__)
# Get json data from the external api
def GetData(brand, date_from, date_to, api_key, limit):
    with requests.Session() as s:
        download = s.get(f"http://api.marketstack.com/v1/eod?access_key={api_key}&symbols={brand}&limit={limit}")
        decoded_content = download.content.decode()
        
        filename = os.path.join(dirname, f"values\{brand}.json")
        open(filename, 'w').write(decoded_content)

if __name__ == '__main__':
    GetData('AAPL', '2020-05-21', '2020-06-21', Config.MARKET_API_KEY, 20)  
    ProcessData(os.path.join(dirname, f"values\AAPL.json"))