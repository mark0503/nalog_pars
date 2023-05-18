import locale

from telebot import types
from dotenv import load_dotenv

from main import bot
from pb_nalog_parser import PbNalogParser
from utils import check_nalog, check_inn, check_pdf

load_dotenv()


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Сведения"),
        types.KeyboardButton("Ограничения"),
        types.KeyboardButton("Выписка")
    )
    bot.send_message(message.chat.id, "Выберите в меню,что вам интересно о компании по ИНН.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Data'))
def welcome(call):
    bot.send_message(call.message.chat.id, "Выберите в меню,что вам интересно о компании по ИНН.")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ['Сведения', 'Ограничения', 'Выписка']:
        if message.text == 'Сведения':
            keyboard = types.InlineKeyboardMarkup()
            url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
            keyboard.add(url_button1)
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(message, check_nalog)
        elif message.text == 'Ограничения':
            keyboard = types.InlineKeyboardMarkup()
            url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
            keyboard.add(url_button1)
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(message, check_inn)
        elif message.text == 'Выписка':
            keyboard = types.InlineKeyboardMarkup()
            url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
            keyboard.add(url_button1)
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(message, check_pdf)
