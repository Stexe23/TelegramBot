import telebot
from extensions import APIException, ValueConvert  # Импорт классов
from config import TOKEN, key  # Импорт ключей бота и валют

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands='start')  # Обработчик начала работы
def start_(message: telebot.types.Message):
    text = 'Приветствую.\n' \
           'Для продолжения введите /help'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands='help')  # Обработчик помощи
def help_(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n <имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<количество переводимой валюты>\n' \
           'Увидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands='values')  # Обработчик списка доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for i in key.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])  # Обработчик конвертора валют
def conver(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:  # Обязательно: три параметра ввода
            raise APIException('Слишком мало/много пораметров')

        resp = ValueConvert.get_price(*value)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, resp)


bot.polling()
