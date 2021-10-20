import datetime
import re
import uuid

import requests


cooks_nalog = {}

response = requests.get('https://kad.arbitr.ru/', headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                                           'Accept-Encoding': 'gzip, deflate, br',
                                                           'Accept-Language': 'ru-RU,ru;q=0.9',
                                                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'})
for cook in response.cookies:
    cooks_nalog[cook.name] = cook.value
response = requests.get('https://kad.arbitr.ru/', headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'},
                        cookies=cooks_nalog)
for cook in response.cookies:
    cooks_nalog[cook.name] = cook.value
data = {
    'name': '7726737421'
}
response = requests.post('https://kad.arbitr.ru/Suggest/GetSidesByName?count=10&suggestType=side',
                         data=data,
                         cookies=cooks_nalog,
                         headers={
                             'Accept': 'application/json, text/javascript, */*',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'ru-RU,ru;q=0.9',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                             'X-Requested-With': 'XMLHttpRequest',
                             'Content-Type': 'application/x-www-form-urlencoded',
                             'Referer': 'https://kad.arbitr.ru/'
                         })
cooks_nalog['wasm'] = str(uuid.uuid4()).replace('-', '')
data = {"Page":'1',"Count":'25',"Courts":[],"DateFrom":"null","DateTo":"null","Sides":[{"Name":"7726737421","Type":'-1',"ExactMatch":False}],"Judges":[],"CaseNumbers":[],"WithVKSInstances":False}
json = {
    "Page": 1,
    "Count": 25,
    "Sides": [
        {
            "Name": "7726737421",
            "Type": -1,
            "ExactMatch": False
        }
    ],
    "WithVKSInstances": False
}
print(response.text)
captcha_img = datetime.datetime.now().timestamp()
captcha_img = str(captcha_img)[:-2].replace('.', '')

params = {
    '_': captcha_img
}

print(captcha_img)
response = requests.get('https://kad.arbitr.ru/Recaptcha/IsNeedShowCaptcha', params=params, cookies=cooks_nalog, headers={
                             'Accept': 'application/json, text/javascript, */*',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'ru-RU,ru;q=0.9',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                             'X-Requested-With': 'XMLHttpRequest',
                             'Referer': 'https://kad.arbitr.ru/'
                         })
print(response.text)
response = requests.get('https://kad.arbitr.ru/Recaptcha/IsNeedShowCaptcha', params=params, cookies=cooks_nalog, headers={
                             'Accept': 'application/json, text/javascript, */*',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'ru-RU,ru;q=0.9',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                             'X-Requested-With': 'XMLHttpRequest',
                             'Referer': 'https://kad.arbitr.ru/'
                         })
print(response.text)
for cook in response.cookies:
    cooks_nalog[cook.name] = cook.value
print(cooks_nalog)
response = requests.post('https://kad.arbitr.ru/Kad/SearchInstances', json=json, cookies=cooks_nalog, headers={
                             'Accept': '*/*',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'ru-RU,ru;q=0.9',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                             'X-Requested-With': 'XMLHttpRequest',
                             'Referer': 'https://kad.arbitr.ru/',
                             'x-date-format': 'iso',
                             'Content-Type': 'application/json'

                         })
