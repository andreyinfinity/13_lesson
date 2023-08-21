import requests
import json
import os.path
from datetime import datetime


def download_json(url: str) -> dict | list:
    return requests.get(url).json()


def save_file(filename: str, array: dict) -> None:
    """

    :rtype: object
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(array, file, ensure_ascii=False, indent=4)


def open_file(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def check_file(filename: str) -> bool:
    return os.path.exists(filename)


def check_date(date_in_file) -> bool:
    return str(datetime.now().date()) == date_in_file


def get_keys(dictionary, key):
    all_keys = ""
    keys = dictionary.get(key).keys()
    for item in keys:
        all_keys += "/" + item + ", "
    return all_keys


def get_rate(dictionary, currency_symbol):
    rate = round(float(dictionary.get("rates").get("RUB") / dictionary.get("rates").get(currency_symbol.upper())), 2)
    return f'1 {currency_symbol.upper()} = {rate} RUB'


def get_currency_name(dictionary, currency_symbol):
    return f'{currency_symbol} - {dictionary.get("symbols").get(currency_symbol)}'
