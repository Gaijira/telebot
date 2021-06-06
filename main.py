import telebot
import requests
import pandas

bot = telebot.TeleBot("775660511:AAH_RTkqVUsT9sEK5W7CpE1JdTepfVYjObQ", parse_mode=None)


@bot.message_handler(commands=['find_crypto_rate', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Choose crypto to show?")


seven_days_rates = []


@bot.message_handler(func=lambda message: True)
def currency_handler(message):
    needed_currency = str(message.text).lower()
    req = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price?ids=' + needed_currency + '&vs_currencies=usd')
    answ = req.json()[needed_currency]['usd']
    bot.send_message(message.chat.id, f'Current {message.text} rate is: \n\n{answ}$')
    daily_rate = requests.get(
        f'https://api.coingecko.com/api/v3/coins/' + needed_currency + '/market_chart?vs_currency=usd&days=7&interval=daily')
    seven_days_rates.extend([int(item[1]) for item in daily_rate.json()['prices']])
    print(seven_days_rates)
    s = pandas.Series(seven_days_rates), dtype=pandas.StringDtype())
    s.plot.line()



bot.polling()
