import requests
import json
from datetime import datetime

CURRENCY_RATES_FILE = 'data/currency_rates.json'
CURRENCY_SYMBOLS_FILE = 'data/currency_symbols.json'
API_KEY = '4e94ffc3559fdde73bd0251a742a339b'
base_currency = 'RUB'
output_currency = 'USD,EUR,RUB'


url = f"http://api.exchangeratesapi.io/v1/symbols?access_key={API_KEY}"
print(url)
response = requests.get(url)
request = response.json()
print(response)

print(request)

with open('currency.json', 'w', encoding='utf-8') as file:
    json.dump(request, file, ensure_ascii=False, indent=4)
