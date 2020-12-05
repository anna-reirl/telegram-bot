import telebot
import json
import requests

TOKEN = '1430747342:AAEvIc85jS3rWwRiQ8Ei8r6d_KUh1eB3pak'

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
}


@bot.message_handler(commands=['start','help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \ ' \
'на какую валюту перевести> \'' \
'<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    queto, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[queto]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {queto} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()