import telebot
from telebot import types

token = '734653465:AAGLuLdQ9CByJvHNsFOKRtH6Y-wME6ZH2n0'

bot = telebot.TeleBot(token)

currencies = ['евро', 'доллар']

def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=c, callback_data=c)
     for c in currencies]
    keyboard.add(*buttons)
    return keyboard

@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    message = callback_query.message
    text = callback_query.data
    currency, value = check_currency_value(text)
    if currency:
        bot.answer_callback_query(callback_query.id, text='Курс {} равен {}'.format(currency, value))
        # bot.send_message(chat_id=message.chat.id, text='Курс {} равен {}'.format(currency, value))
    else:
        bot.send_message(chat_id=message.chat.id, text='Узнай курс валют.')

def closeset_bank(location):
    lat = location.latitude
    lon = location.longitude
    bank_address = 'ул. Гринченка, 9'
    bank_lat, bank_lon = 55.800388, 37.543710
    return bank_address, bank_lat, bank_lon

def check_currency(message):
    for c in currencies:
        if message.text is not None and c in message.text.lower():
            return True
    return False


def check_currency_value(text):
    currency_values = {'евро': 70, 'доллар': 60}
    for currency, value in currency_values.items():
        if currency in text.lower():
            return currency, value
    return None, None


@bot.message_handler(commands=['rate'])
@bot.message_handler(func=check_currency)
def handle_currency(message):
    currency, value = check_currency_value(message.text)
    keyboard = create_keyboard()
    if currency:
        bot.send_message(chat_id=message.chat.id, text='Курс {} равен {}'.format(currency, value), reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text='Узнай курс валют.', reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print(message.location)
    bank_address, bank_lat, bank_lon = closeset_bank(message.location)
    images = open('cat-snow.jpg', 'rb')
    bot.send_message(chat_id=message.chat.id, text='Ближайший банк {}'.format(bank_address))
    bot.send_photo(message.chat.id, images, caption='Ближайший банк {}'.format(bank_address))
    bot.send_location(message.chat.id, bank_lat, bank_lon)

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Узнай курс валют.')


bot.polling()