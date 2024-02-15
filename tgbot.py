import telebot
import requests
from decouple import config


TOKEN = config('TOKEN')


bot = telebot.TeleBot(TOKEN)


def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangeratesapi.io/latest?base={from_currency}&symbols={to_currency}"
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        print(f"API Error: {data['error']}")
        return None
    rate = data['rates'][to_currency]
    return rate

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для конвертации валют. Используй /help для получения списка команд.')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Доступные команды:\n'
                                      '/start - приветствие и описание бота\n'
                                      '/help - список доступных команд\n'
                                      '/convert  конвертация валюты')


@bot.message_handler(commands=['convert'])
def handle_convert(message):
    try:

        args = message.text.split()[1:]
        amount = float(args[0])
        from_currency = args[1].upper()
        to_currency = args[3].upper()


        rate = get_exchange_rate(from_currency, to_currency)

        if rate is not None:
            converted_amount = amount * rate
            bot.send_message(message.chat.id, f'{amount} {from_currency} = {converted_amount} {to_currency}')
        else:
            bot.send_message(message.chat.id, 'Ошибка при получении курса валюты. Пожалуйста, проверьте правильность ввода.')

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, 'Неверный формат команды. Используйте /convert <amount> <from_currency> to <to_currency>')


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text.lower()
    if 'привет' in text:
        bot.send_message(message.chat.id, 'Привет! Как я могу помочь?')
    elif 'пока' in text:
        bot.send_message(message.chat.id, 'До свидания! Если у вас есть вопросы, вы всегда можете вернуться.')

