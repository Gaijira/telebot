import os
import telebot
import requests
import matplotlib
import matplotlib.pyplot as plt
from datetime import date, timedelta

bot = telebot.TeleBot("775660511:AAH_RTkqVUsT9sEK5W7CpE1JdTepfVYjObQ", parse_mode=None)
matplotlib.pyplot.switch_backend('Agg')


@bot.message_handler(commands=['find_crypto_rate'])
def send_welcome(message):
    bot.send_message(message.chat.id, "What crypto do you want to see?")


@bot.message_handler(content_types=['text'])
def currency_handler(message):
    if message.text.lower() not in ['yes', 'no']:
        needed_currency = str(message.text).lower()
        req = requests.get(
            f'https://api.coingecko.com/api/v3/simple/price?ids=' +
            needed_currency +
            '&vs_currencies=usd')
        answ = req.json()[needed_currency]['usd']
        daily_rate = requests.get(
            f'https://api.coingecko.com/api/v3/coins/' +
            needed_currency +
            '/market_chart?vs_currency=usd&days=6&interval=daily')
        seven_days_rates = [float(item[1]) for item in daily_rate.json()['prices']]
        graph_builder(dates_getter(), seven_days_rates)
        bot.send_message(message.chat.id, f'Current {message.text} rate is: \n\n{answ}$')
        bot.send_message(message.chat.id, f'Do you want to see {message.text} line chart?')
    elif message.text.lower() == 'yes':
        if 'fig.png':
            bot.send_photo(message.chat.id, open('fig.png', 'rb'))
            os.remove('fig.png')
    else:
        bot.send_message(message.chat.id, 'Terminate...')


def dates_getter():
    days = []
    i = 0
    while i != 7:
        days.append((date.today() - timedelta(days=i)).strftime("%m.%d"))
        i += 1
    x = sorted(days, reverse=False)
    return x


def graph_builder(dates, rates):
    plt.plot(dates, rates)
    plt.title("7 Days Graph")
    plt.xlabel("Dates")
    plt.ylabel("Price")
    plt.grid()
    plt.savefig('fig.png')
    plt.close()


bot.polling(none_stop=True, interval=0)
