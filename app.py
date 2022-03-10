import json
import telebot
import requests
from config import TOKEN, key

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def set_welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n <имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<количество переводимой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands='values')
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for i in key.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def conver(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={key[quote]}&tsyms={key[base]}')
    resp = json.loads(r.content)[key[base]]
    text = f'Итого: {amount} {quote} равна {resp} {base}'
    bot.send_message(message.chat.id, text)


bot.polling()
