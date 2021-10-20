import requests
import uuid


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
cooks = {}
response = requests.get('https://service.nalog.ru/bi.html', headers=headers)
for cook in response.cookies:
    cooks[cook.name] = cook.value
data = {
    'requestType': 'FINDPRS',
    'innPRS': '7726737421',
    'bikPRS': '044525555',
    'fileName': '',
    'bik': '',
    'kodTU': '',
    'dateSAFN': '',
    'bikAFN': '',
    'dateAFN': '',
    'fileNameED': '',
    'captcha': '',
    'captchaToken': ''
}
response = requests.post('https://service.nalog.ru/bi2-proc.json', data=data, headers=headers, cookies=cooks).json()
rows = response['rows']
print(f'{rows[0]["NAIM"]} имеет {len(rows)} арестов счетов')
i = 1
for row in rows:
    print(f'№{i}:')
    print(f'номер решения о приостановлении: {row["NOMER"]}')
    print(f'Дата решения о приостановлении: {row["DATA"]}')
    print(f'Код основания: {row["KODOSNOV"]}')
    print(f'код налогового органа: {row["IFNS"]}')
    print(f'БИК банка: {row["BIK"]}')
    print(f'Дата и время размещения информации: {row["DATABI"]}')
    print('---------------')
    i += 1
