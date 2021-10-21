import locale
import re
from pathlib import Path
import os

import requests
import telebot
from telebot import types
from dotenv import load_dotenv
import time


load_dotenv()
token_tg = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token_tg)
tokens = {}
cooks = {}
inn = {}
cooks_nalog = {}
headers = {}
token_inn = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mrk = types.KeyboardButton("Сведения")
    mrk1 = types.KeyboardButton("Ограничения")
    mrk2 = types.KeyboardButton("Выписка")
    markup.add(mrk, mrk1, mrk2)
    bot.send_message(message.chat.id, "Выберите в меню,что вам интересно о компании по ИНН.", reply_markup=markup)
    while True:
        requests.get('https://colorscheme.ru/')
        time.sleep(900)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ['Сведения', 'Ограничения', 'Выписка']:
        if message.text == 'Сведения':
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html'
            )
            bot.register_next_step_handler(message, check_nalog)
        elif message.text == 'Ограничения':
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html'
            )
            bot.register_next_step_handler(message, check_inn)
        elif message.text == 'Выписка':
            bot.send_message(
                message.from_user.id,
                'Введите ИНН организации',
                parse_mode='html'
            )
            bot.register_next_step_handler(message, check_pdf)


def check_nalog(message):
    if len(message.text) != 12 and len(message.text) != 10:
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_nalog)
    elif not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_nalog)
    else:
        inn[2] = message.text
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        response = requests.get('https://pb.nalog.ru/', headers=headers)
        for cook in response.cookies:
            cooks_nalog[cook.name] = cook.value
        response = requests.get('https://pb.nalog.ru/search.html', headers=headers, cookies=cooks_nalog)
        for cook in response.cookies:
            cooks_nalog[cook.name] = cook.value
        data = {
            'method': 'get-lst'
        }
        response = requests.post('https://pb.nalog.ru/compare-proc.json', data=data, headers=headers, cookies=cooks_nalog)
        for cook in response.cookies:
            cooks_nalog[cook.name] = cook.value
        headers['X-Requested-With'] = 'XMLHttpRequest'
        data = {
            'page': 1,
            'pageSize': 10,
            'mode': 'search-all',
            'queryAll': message.text,
            'mspUl1': 1,
            'mspUl2': 2,
            'mspUl3': 3,
            'mspIp1': 1,
            'mspIp2': 2,
            'mspIp3': 3,
            'uprType1': 1,
            'uprType0': 1,
            'ogrFl': 1,
            'ogrUl': 1,
            'npTypeDoc': 1,
        }
        response = requests.post('https://pb.nalog.ru/search-proc.json', data=data, headers=headers, cookies=cooks_nalog)
        if 'ERROR' in response.json():
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = requests.get('https://pb.nalog.ru/captcha-dialog.html', params=params, headers=headers,
                                    cookies=cooks_nalog).text
            token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            tokens[2] = token
            params = {
                'a': token,
                'version': 2
            }
            url = 'https://pb.nalog.ru/static/captcha.bin'
            img = requests.get(url=url, params=params, headers=headers, cookies=cooks_nalog)
            img_file = open("img.jpg", "wb")
            img_file.write(img.content)
            img_file.close()
            bot.send_message(
                message.from_user.id,
                'введите капчу',
                parse_mode='html'
            )
            bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
            bot.register_next_step_handler(message, captcha_resolve)
        else:
            token_inn[0] = response.json()['ul']['data'][0]['token']
            response = requests.get(f'https://pb.nalog.ru/company.html?token={token_inn[0]}', headers=headers, cookies=cooks_nalog)
            for cook in response.cookies:
                cooks_nalog[cook.name] = cook.value
            data = {
                'token': token_inn[0],
                'method': 'get-request'
            }
            response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers, cookies=cooks_nalog)
            if 'ERROR' in response.json():
                params = {
                    'aver': '2.7.58',
                    'sver': '4.38.63',
                    'pageStyle': 'GM2'
                }
                response = requests.get('https://pb.nalog.ru/captcha-dialog.html', params=params, headers=headers,
                                        cookies=cooks_nalog).text
                token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
                tokens[2] = token
                params = {
                    'a': token,
                    'version': 2
                }
                url = 'https://pb.nalog.ru/static/captcha.bin'
                img = requests.get(url=url, params=params, headers=headers, cookies=cooks_nalog)
                img_file = open("img.jpg", "wb")
                img_file.write(img.content)
                img_file.close()
                bot.send_message(
                    message.from_user.id,
                    'введите капчу',
                    parse_mode='html'
                )
                bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
                bot.register_next_step_handler(message, captcha_resolve_2)
            else:
                id = response.json()['id']
                token = response.json()['token']
                data = {
                    'token': token,
                    'id': id,
                    'method': 'get-response'
                }
                headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers, cookies=cooks_nalog)
                print(response.text)
                result_parse(message=message, mes=response.json())


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


def captcha_resolve_2(message):
    data = {
        'captcha': message.text,
        'captchaToken': tokens[2]
    }
    response = requests.post('https://pb.nalog.ru/captcha-proc.json', data=data, headers=headers,
                             cookies=cooks_nalog)
    if 'ERROR' in response.text:
        bot.send_message(
            message.from_user.id,
            'НЕВЕРНО, ПОВТОРИТЕ ПОПЫТКУ',
            parse_mode='html'
        )
        params = {
            'aver': '2.7.58',
            'sver': '4.38.63',
            'pageStyle': 'GM2'
        }
        response = requests.get('https://pb.nalog.ru/captcha-dialog.html', params=params, headers=headers,
                                cookies=cooks_nalog).text
        token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
        tokens[2] = token
        params = {
            'a': token,
            'version': 2
        }
        url = 'https://pb.nalog.ru/static/captcha.bin'
        img = requests.get(url=url, params=params, headers=headers, cookies=cooks_nalog)
        img_file = open("img.jpg", "wb")
        img_file.write(img.content)
        img_file.close()
        bot.send_message(
            message.from_user.id,
            'введите капчу',
            parse_mode='html'
        )
        bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
        bot.register_next_step_handler(message, captcha_resolve_2)
    else:
        token = re.findall(r'"(.*)"', response.text)[0]
        data = {
            'token': token_inn[0],
            'method': 'get-request',
            'pbCaptchaToken': token
        }
        response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers,
                                 cookies=cooks_nalog)
        id = response.json()['id']
        token = response.json()['token']
        data = {
            'token': token,
            'id': id,
            'method': 'get-response'
        }
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers,
                                 cookies=cooks_nalog)
        result_parse(message=message, mes=response.json())


def captcha_resolve(message):
    data = {
        'captcha': message.text,
        'captchaToken': tokens[2]
    }
    response = requests.post('https://pb.nalog.ru/captcha-proc.json', data=data, headers=headers,
                             cookies=cooks_nalog)
    if 'ERROR' in response.text:
        params = {
            'aver': '2.7.58',
            'sver': '4.38.63',
            'pageStyle': 'GM2'
        }
        response = requests.get('https://pb.nalog.ru/captcha-dialog.html', params=params, headers=headers,
                                cookies=cooks_nalog).text
        token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
        tokens[2] = token
        params = {
            'a': token,
            'version': 2
        }
        url = 'https://pb.nalog.ru/static/captcha.bin'
        img = requests.get(url=url, params=params, headers=headers, cookies=cooks_nalog)
        img_file = open("img.jpg", "wb")
        img_file.write(img.content)
        img_file.close()
        bot.send_message(
            message.from_user.id,
            'введите капчу',
            parse_mode='html'
        )
        bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
        bot.register_next_step_handler(message, captcha_resolve)
    else:
        token = re.findall(r'"(.*)"', response.text)[0]
        data = {
            'page': 1,
            'pageSize': 10,
            'mode': 'search-all',
            'queryAll': inn[2],
            'pbCaptchaToken': token,
            'mspUl1': 1,
            'mspUl2': 2,
            'mspUl3': 3,
            'mspIp1': 1,
            'mspIp2': 2,
            'mspIp3': 3,
            'uprType1': 1,
            'uprType0': 1,
            'ogrFl': 1,
            'ogrUl': 1,
            'npTypeDoc': 1,
        }
        response = requests.post('https://pb.nalog.ru/search-proc.json', data=data, headers=headers,
                                 cookies=cooks_nalog)
        token_inn[0] = response.json()['ul']['data'][0]['token']
        response = requests.get(f'https://pb.nalog.ru/company.html?token={token_inn[0]}', headers=headers, cookies=cooks_nalog)
        for cook in response.cookies:
            cooks_nalog[cook.name] = cook.value
        data = {
            'token': token_inn[0],
            'method': 'get-request'
        }
        response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers, cookies=cooks_nalog)
        if 'ERROR' in response.json():
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = requests.get('https://pb.nalog.ru/captcha-dialog.html', params=params, headers=headers,
                                    cookies=cooks_nalog).text
            token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            tokens[2] = token
            params = {
                'a': token,
                'version': 2
            }
            url = 'https://pb.nalog.ru/static/captcha.bin'
            img = requests.get(url=url, params=params, headers=headers, cookies=cooks_nalog)
            img_file = open("img.jpg", "wb")
            img_file.write(img.content)
            img_file.close()
            bot.send_message(
                message.from_user.id,
                'введите капчу',
                parse_mode='html'
            )
            bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
            bot.register_next_step_handler(message, captcha_resolve_2)
        else:
            id = response.json()['id']
            token = response.json()['token']
            data = {
                'token': token,
                'id': id,
                'method': 'get-response'
            }
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            response = requests.post('https://pb.nalog.ru/company-proc.json', data=data, headers=headers, cookies=cooks_nalog)
            result_parse(message=message, mes=response.json())


def check_pdf(message):
    if len(message.text) != 12 and len(message.text) != 10:
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_pdf)
    elif not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_pdf)
    else:
        re = bot.send_message(
            message.from_user.id,
            'Идет загрузка...',
            parse_mode='html'
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        params = {
            'query': message.text,
            'page': 0
        }
        response = requests.get('https://bo.nalog.ru/nbo/organizations/search', params=params, headers=headers)
        id = response.json()['content'][0]['id']
        filename = Path('metadata.pdf')
        url = f'https://bo.nalog.ru/download/bfo/pdf/{id}?period=2020'
        response = requests.get(url=url, headers=headers)
        filename.write_bytes(response.content)
        f = open("metadata.pdf", "rb")
        bot.edit_message_text('Загрузка завершена.', message_id=re.message_id, chat_id=message.from_user.id)
        bot.send_document(message.from_user.id, f)


def check_inn(message):
    if len(message.text) != 12 and len(message.text) != 10:
        bot.send_message(
            message.from_user.id,
            'ИНН содержит 10-12 символов, повторите попытку.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_nalog)
    elif not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            'ИНН содержит только цифры.',
            parse_mode='html'
        )
        bot.register_next_step_handler(message, check_inn)
    else:
        inn[1] = message.text
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        response = requests.get('https://service.nalog.ru/bi.html', headers=headers)
        for cook in response.cookies:
            cooks[cook.name] = cook.value

        response = requests.get('https://service.nalog.ru/static/captcha-dialog.html?aver=3.40.10&sver=4.38.62&pageStyle=GM2', headers=headers, cookies=cooks).text
        token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
        tokens[1] = token
        params = {
            'a': token,
            'version': 2
        }
        url = 'https://service.nalog.ru/static/captcha.bin'
        img = requests.get(url=url, params=params, headers=headers, cookies=cooks)
        img_file = open("img.jpg", "wb")
        img_file.write(img.content)
        img_file.close()
        bot.send_message(
            message.from_user.id,
            'введите капчу',
            parse_mode='html'
        )
        bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
        bot.register_next_step_handler(message, check_captcha)


def check_captcha(message):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    data = {
        'captcha': message.text,
        'captchaToken': tokens[1]
    }
    response = requests.post('https://service.nalog.ru/static/captcha-proc.json', data=data, headers=headers, cookies=cooks)
    if 'ERROR' in response.text:
        response = requests.get(
            'https://service.nalog.ru/static/captcha-dialog.html?aver=3.40.10&sver=4.38.62&pageStyle=GM2',
            headers=headers, cookies=cooks).text
        token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
        tokens[1] = token
        params = {
            'a': token,
            'version': 2
        }
        url = 'https://service.nalog.ru/static/captcha.bin'
        img = requests.get(url=url, params=params, headers=headers, cookies=cooks)
        img_file = open("img.jpg", "wb")
        img_file.write(img.content)
        img_file.close()
        bot.send_message(
            message.from_user.id,
            'введите капчу',
            parse_mode='html'
        )
        bot.send_photo(message.from_user.id, photo=open('img.jpg', 'rb'))
        bot.register_next_step_handler(message, check_captcha)
    else:
        token = re.findall(r'"(.*)"', response.text)[0]
        data = {
            'requestType': 'FINDPRS',
            'innPRS': inn[1],
            'bikPRS': '044525174',
            'fileName': '',
            'bik': '',
            'kodTU': '',
            'dateSAFN': '',
            'bikAFN': '',
            'dateAFN': '',
            'fileNameED': '',
            'captcha': '',
            'captchaToken': token
        }
        response = requests.post('https://service.nalog.ru/bi2-proc.json', data=data, headers=headers, cookies=cooks).json()
        print(response)
        rows = response.get('rows')
        if rows:
            rows = response['rows']
            bot.send_message(message.chat.id, f'{rows[0]["NAIM"]} имеет {len(rows)} арестов счетов')
            i = 1
            for row in rows:
                text = f"""<b>№{i}:</b> 
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
                i += 1
            if len(rows) == 0:
                bot.send_message(message.chat.id, f'{rows[0]["NAIM"]} имеет {len(rows)} арестов счетов')


bot.polling()
