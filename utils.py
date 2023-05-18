import locale

from telebot import types

from main import bot
from pb_nalog_parser import PbNalogParser


def check_nalog(message):
    if len(message.text) != 12 and len(message.text) != 10:
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        keyboard.add(url_button1)
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_nalog)
    elif not message.text.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        )
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_nalog)
    else:
        nalog_parser = PbNalogParser(message.text)

        get_info, captcha, captcha_token = nalog_parser.check_nalog_step_1()
        if captcha:
            bot.send_photo(message.from_user.id, photo=captcha)
            bot.register_next_step_handler(message, captcha_resolve, nalog_parser, captcha_token)
        else:
            token = get_info['ul']['data'][0]['token']
            get_info, captcha = nalog_parser.check_nalog_step_2(token)
            if captcha:
                bot.send_photo(message.from_user.id, photo=captcha)
                bot.register_next_step_handler(message, captcha_resolve_2)
            else:
                result = nalog_parser.get_info(get_info['id'], get_info['token'])
                result_parse(message=message, mes=result)


def captcha_resolve(message, nalog_parser, captcha_token):
    get_info, captcha_v1, captcha_v2, captcha_token = nalog_parser.captcha_resolve(message.text, captcha_token)
    if captcha_v1:
        bot.send_photo(message.from_user.id, photo=captcha_v1)
        bot.register_next_step_handler(message, captcha_resolve, nalog_parser, captcha_token)
    elif captcha_v2:
        bot.send_photo(message.from_user.id, photo=captcha_v2)
        bot.register_next_step_handler(message, captcha_resolve_2, nalog_parser, captcha_token)
    else:
        result = nalog_parser.get_info(get_info['id'], get_info['token'])
        result_parse(message=message, mes=result)


def captcha_resolve_2(message, nalog_parser, captcha_token):
    get_info, captcha, captcha_token = nalog_parser.captcha_resolve(message.text, captcha_token)
    if captcha:
        bot.send_photo(message.from_user.id, photo=captcha)
        bot.register_next_step_handler(message, captcha_resolve_2, nalog_parser, captcha_token)
    else:
        result = nalog_parser.get_info(get_info['id'], get_info['token'])
        result_parse(message=message, mes=result)


def check_pdf(message):
    if len(message.text) != 12 and len(message.text) != 10:
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        keyboard.add(url_button1)
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_pdf)
    elif not message.text.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        keyboard.add(url_button1)
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_pdf)
    else:
        start = bot.send_message(
            message.from_user.id,
            'Идет загрузка...',
            parse_mode='html'
        )
        nalog_parser = PbNalogParser(message.text)
        result_pdf = nalog_parser.get_pdf()
        bot.edit_message_text('Загрузка завершена.', message_id=start.message_id, chat_id=message.from_user.id)
        bot.send_document(message.from_user.id, result_pdf)


def check_inn(message):
    if len(message.text) != 12 and len(message.text) != 10:
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        keyboard.add(url_button1)
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_nalog)
    elif not message.text.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Отмена.", callback_data='Data')
        keyboard.add(url_button1)
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, check_inn)
    else:
        nalog_parser = PbNalogParser(message.text)
        get_info, captcha, captcha_token = nalog_parser.check_inn()
        bot.send_photo(message.from_user.id, photo=captcha)
        bot.register_next_step_handler(message, check_captcha, nalog_parser, captcha_token)


def check_captcha(message, nalog_parser, token):
    get_info, captcha, captcha_token = nalog_parser.check_captcha_for_inn(message.text, token)
    if captcha:
        bot.send_photo(message.from_user.id, photo=captcha)
        bot.register_next_step_handler(message, captcha_resolve_2, nalog_parser, captcha_token)
    else:
        for row in get_info:
            text = f"""
                    <b>номер решения о приостановлении: {row["NOMER"]}</b> 
                    <b>Дата решения о приостановлении: {row["DATA"]}</b> 
                    <b>Код основания: {row["KODOSNOV"]}</b> 
                    <b>код налогового органа: {row["IFNS"]}</b> 
                    <b>ИК банка: {row["BIK"]}</b> 
                    <b>Дата и время размещения информации: {row["DATABI"]}</b> 
                    ------------"""
            bot.send_message(
                message.from_user.id,
                text,
                parse_mode='html'
            )
        if len(get_info) == 0:
            bot.send_message(message.chat.id, f'{get_info[0]["NAIM"]} имеет {len(get_info)} арестов счетов')


def result_parse(message, mes):
    locale.setlocale(locale.LC_ALL, '')
    try:
        revenuesum = (locale.format('%d', int(mes['vyp']['revenuesum']), grouping=True))
        expensesum = (locale.format('%d', int(mes['vyp']['expensesum']), grouping=True))
        text = f"""<b>Название полное:{mes['vyp']['НаимЮЛПолн']}</b> 
                <b>Адрес:{mes['vyp']['Адрес']}</b> 
                <b>Название сокращенное:{mes['vyp']['НаимЮЛСокр']}</b> 
                <b>ОГРН: {mes['vyp']['ОГРН']}</b> 
                <b>Дата регистрации:{mes['vyp']['ДатаПостУч']}</b> 
                <b>ОКВЭД: {mes['vyp']['НаимОКВЭД']}</b> 
                <b>Среднесписочная численность работников организации: {mes['vyp']['sschr']}</b> 
                <b>Суммы доходов: {revenuesum}</b> 
                <b>Суммы разходов: {expensesum}</b> 
                ------------"""

        bot.send_message(
            message.from_user.id,
            text,
            parse_mode='html'
        )
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Повторите попытку еще раз',
            parse_mode='html'
        )

