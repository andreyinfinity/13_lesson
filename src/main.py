import os
import telebot
from utils.functions import (save_file, open_file, download_json, check_file, check_date, get_keys, get_rate,
                             get_currency_name)

CURRENCY_RATES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'currency_rates.json')
CURRENCY_SYMBOLS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'currency_symbols.json')
API_KEY = '4e94ffc3559fdde73bd0251a742a339b'
url_symbols = f"http://api.exchangeratesapi.io/v1/symbols?access_key={API_KEY}"
url_latest = f"http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}"

# Подключаем токен бота
bot = telebot.TeleBot('6585601634:AAFn5nTtf5JR4KF6UNsOmTN3rN1GJxL9JI8')


# Обработка команд, полученных от бота
@bot.message_handler(commands=['start', 'help', 'currency'])
def command(message):
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id,  f"Привет, {message.from_user.first_name}.\n"
                                                f"Для получения списка команд набери /help")
    elif message.text.lower() == '/help':
        to_pin = bot.send_message(message.from_user.id,  "Для получения курса введите сокращенное название "
                                                "валюты, состоящее из 3 букв.\n"
                                                "Команда /currency - выводит все возможные валюты для конвертации.\n"
                                                "Популярные валюты: /USD, /EUR, /CNY.").message_id
        bot.pin_chat_message(message.chat.id, to_pin)
    elif message.text.lower() == '/currency':
        currency_symbols_str = get_keys(currency_symbols, 'symbols')
        bot.send_message(message.from_user.id, currency_symbols_str)


# Обмен текстовыми сообщениями
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text.upper().lstrip('/') in get_keys(currency_rates, 'rates'):
        bot.send_message(message.from_user.id, get_currency_name(currency_symbols, message.text.lstrip('/')))
        bot.send_message(message.from_user.id, get_rate(currency_rates, message.text.lstrip('/')))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# Проверяем есть ли файл с описанием всех валют. Если нет, то загружаем его.
if not check_file(CURRENCY_SYMBOLS_FILE):
    os.mkdir('data')
    save_file(CURRENCY_SYMBOLS_FILE, download_json(url_symbols))

currency_symbols = open_file(CURRENCY_SYMBOLS_FILE)

# Проверяем есть ли файл с курсом всех валют. Если нет, то загружаем его.
if not check_file(CURRENCY_RATES_FILE):
    save_file(CURRENCY_RATES_FILE, download_json(url_latest))

# Проверяем дату получения последнего курса валюты. Если даты не совпадают, то загружаем курс валют.
currency_rates = open_file(CURRENCY_RATES_FILE)
if not check_date(currency_rates.get("date")):
    save_file(CURRENCY_RATES_FILE, download_json(url_latest))

bot.polling(none_stop=True, interval=0)
