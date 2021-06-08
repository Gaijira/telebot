import os
import time
import telebot
import requests
import matplotlib
import matplotlib.pyplot as plt

bot = telebot.TeleBot("775660511:AAH_RTkqVUsT9sEK5W7CpE1JdTepfVYjObQ", parse_mode=None)
matplotlib.pyplot.switch_backend('Agg')


@bot.message_handler(commands=['find_crypto_rate'])
def send_welcome(message):
    print(message)
    bot.send_message(message.chat.id, "Choose crypto to show?")


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
        plt.plot(['Mon', 'Tue', 'Wend', 'Thur', 'Fri', 'Sun', 'Sat'], seven_days_rates)
        plt.savefig('fig.png')
        plt.close()
        time.sleep(3)
        bot.send_message(message.chat.id, f'Current {message.text} rate is: \n\n{answ}$')
        time.sleep(3)
        bot.send_message(message.chat.id, f'Do you want to see {message.text} line chart?')
    elif message.text.lower() == 'yes':
        if 'fig.png':
            bot.send_photo(message.chat.id, open('fig.png', 'rb'))
            os.remove('fig.png')
    else:
        bot.send_message(message.chat.id, 'Fuck off than!')


bot.polling(none_stop=True, interval=0)
