from config import key
import requests
import json


class APIException(Exception):  # Класс ошибок
    pass


class ValueConvert:  # Класс для конверитрования волюты
    @staticmethod
    def get_price(quote: str, base: str, amount: str):  # Функция обработки конвертируемых волют
        try:
            quote_ticker = key[quote.lower()]  # Переводимая валюта. Понижаем регистр напсания
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        if quote == base:  # Если валюта одна и таже
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            base_ticker = key[base.lower()]  # Получаемая валюта. Понижаем регистр написания
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            amount = float(amount)  # Число с плавоющей точкой
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        resp = json.loads(r.content)
        resp_sum = resp[base_ticker] * amount  # Вычислеение значений после конвертации валюты
        resp_sum = round(resp_sum, 4)  # Округление до 4 знаков после запятой
        message = f"Цена {amount} {quote} в {base} : {resp_sum}"

        return message
