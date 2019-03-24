import telebot
token = '734653465:AAGLuLdQ9CByJvHNsFOKRtH6Y-wME6ZH2n0'

bot = telebot.TeleBot(token)

currencies = ['евро', 'доллар']


def check_currency(message):
    for c in currencies:
        if c in message.text.lower():
            return True
    return False


def check_currency_value(text):
    currency_values = {'евро': 70, 'доллар': 60}
    for currency, value in currency_values.items():
        if currency in text.lower():
            return currency, value
    return None, None


@bot.message_handler(func=check_currency)
def handle_currency(message):
    print(message.text)
    currency, value = check_currency_value(message.text)
    if currency:
        bot.send_message(chat_id=message.chat.id, text='Курс {} равен {}'.format(currency, value))
    else:
        bot.send_message(chat_id=message.chat.id, text='Узнай курс валют.')


@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Узнай курс валют.')


bot.polling()