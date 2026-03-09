import telebot
from telebot import types
import requests

bot = telebot.TeleBot('8499612160:AAF3iYscG_hWWoKBHpbvlzqVdmi35VLzw9o')

@bot.message_handler(commands = ['start'])
def start(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('USD(доллар)')
  btn2 = types.KeyboardButton('EUR(евро)')
  btn3 = types.KeyboardButton('Криптовалюты')
  btn4 = types.KeyboardButton('Конвертер')
  markup.add(btn1,btn2)
  markup.add(btn3, btn4)

  bot.send_message(message.chat.id, 'Зравствуйте! Вы попали в бот по слежке за криптовалютмами и финансовыми вопросами.\nВыберите кнопку или напишите команду ', reply_markup = markup)


@bot.message_handler(func=lambda message: message.text == 'USD(доллар)')
def usd(message):
  url = "https://api.exchangerate-api.com/v4/latest/USD"
  data = requests.get(url).json()

  eur = data['rates']['EUR']
  rub = data['rates']['RUB']

  bot.send_message(message.chat.id, 'Курсы доллара на сегодняшней день: ')
  bot.send_message(message.chat.id,f'Доллар:\n\n1 USD = {eur} EUR\n1 USD = {rub} RUB')

@bot.message_handler(func=lambda message: message.text == 'EUR(евро)')
def eur(message):
  url = "https://api.exchangerate-api.com/v4/latest/EUR"
  data = requests.get(url).json()

  usd = data['rates']['USD']
  rub = data['rates']['RUB']

  bot.send_message(message.chat.id, 'Курсы евро на сегодняшней день: ')
  bot.send_message(message.chat.id, f'Евро: \n\n1 EUR = {usd} USD\n1 EUR = {rub} RUB')

@bot.message_handler(func=lambda message: message.text == 'Криптовалюты')
def crypto(message):
  url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd"
  data = requests.get(url).json()

  btc = data['bitcoin']['usd']
  eth = data['ethereum']['usd']
  usdt = data['tether']['usd']

  bot.send_message(message.chat.id, 'Курсы осноых криптовалют на сегодняшней день: ')
  bot.send_message(message.chat.id, f'Криптовалюты:\n\n'
                   f'BTC = {btc}$\n'
                   f'ETH = {eth}$\n'
                   f'USDT = {usdt}$')

@bot.message_handler(func=lambda message: message.text == 'Конвертер')
def convert(message):
     msg = bot.send_message(message.chat.id, 'Введите в формате:\n\n'
                                      '100 USD EUR\n\n'
                                      'Это значит: конвертировать 100 USD в EUR')
     bot.register_next_step_handler(msg, convert)

@bot.message_handler(func=lambda message: len(message.text.split()) == 3)
def convert(message):
  try:
    amount, from_currency, to_currency = message.text.split()

    amount = float(amount)
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    data = requests.get(url).json()

    rate = data['rates'][to_currency]
    result = amount * rate

    bot.send_message(message.chat.id,f'{amount} {from_currency} = {round(result,2)} {to_currency}')

  except Exception as e:
      bot.send_message(message.chat.id,'Ошибка конвертации.\nВведите так:\n\n100 USD EUR')

bot.polling(none_stop=True)

