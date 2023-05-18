import base64
import re

from requests import Session


class PbNalogParser:

    def __init__(self, inn):
        self.inn = inn
        self.session = Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.71 Safari/537.36 '
        }

    def check_nalog_step_1(self):
        self.session.get('https://pb.nalog.ru/')
        self.session.get('https://pb.nalog.ru/search.html')
        data = {
            'method': 'get-lst'
        }
        self.session.post('https://pb.nalog.ru/compare-proc.json', data=data)
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        data = {
            'page': 1,
            'pageSize': 10,
            'mode': 'search-all',
            'queryAll': self.inn,
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
        response = self.session.post('https://pb.nalog.ru/search-proc.json', data=data)

        if 'ERROR' in response.json():
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = self.session.get('https://pb.nalog.ru/captcha-dialog.html', params=params).text
            captcha_token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            params = {
                'a': captcha_token,
                'version': 2
            }
            url = 'https://pb.nalog.ru/static/captcha.bin'
            img = self.session.get(url=url, params=params)
            image_bytes = base64.b64encode(img.content)
            return None, image_bytes, captcha_token
        return response.json(), None, None

    def captcha_resolve(self, captcha_value, captcha_token):
        data = {
            'captcha': captcha_value,
            'captchaToken': captcha_token
        }
        response = self.session.post('https://pb.nalog.ru/captcha-proc.json', data=data)
        if 'ERROR' in response.text:
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = self.session.get('https://pb.nalog.ru/captcha-dialog.html', params=params).text
            captcha_token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            params = {
                'a': captcha_token,
                'version': 2
            }
            url = 'https://pb.nalog.ru/static/captcha.bin'
            img = self.session.get(url=url, params=params)
            image_bytes = base64.b64encode(img.content)
            return None, image_bytes, None, captcha_token
        else:
            token = re.findall(r'"(.*)"', response.text)[0]
            data = {
                'page': 1,
                'pageSize': 10,
                'mode': 'search-all',
                'queryAll': self.inn,
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
            response = self.session.post('https://pb.nalog.ru/search-proc.json', data=data)
            token_inn = response.json()['ul']['data'][0]['token']
            self.session.get(f'https://pb.nalog.ru/company.html?token={token_inn}')
            data = {
                'token': token_inn,
                'method': 'get-request'
            }
            response = self.session.post('https://pb.nalog.ru/company-proc.json', data=data)
            if 'ERROR' in response.json():
                params = {
                    'aver': '2.7.58',
                    'sver': '4.38.63',
                    'pageStyle': 'GM2'
                }
                response = self.session.get('https://pb.nalog.ru/captcha-dialog.html', params=params).text
                captcha_token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
                params = {
                    'a': captcha_token,
                    'version': 2
                }
                url = 'https://pb.nalog.ru/static/captcha.bin'
                img = self.session.get(url=url, params=params)
                image_bytes = base64.b64encode(img.content)
                return None, None, image_bytes, captcha_token
            else:
                return response.json(), None, None

    def captcha_resolve_v2(self, captcha_value, captcha_token):
        data = {
            'captcha': captcha_value,
            'captchaToken': captcha_token
        }
        response = self.session.post('https://pb.nalog.ru/captcha-proc.json', data=data)
        if 'ERROR' in response.text:
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = self.session.get('https://pb.nalog.ru/captcha-dialog.html', params=params).text
            captcha_token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            params = {
                'a': captcha_token,
                'version': 2
            }
            url = 'https://pb.nalog.ru/static/captcha.bin'
            img = self.session.get(url=url, params=params)
            image_bytes = base64.b64encode(img.content)
            return None, image_bytes, None, captcha_token
        else:
            token = re.findall(r'"(.*)"', response.text)[0]
            data = {
                'token': self.inn,
                'method': 'get-request',
                'pbCaptchaToken': token
            }
            response = self.session.post('https://pb.nalog.ru/company-proc.json', data=data)
            data = {
                'token': response.json()['token'],
                'id': response.json()['id'],
                'method': 'get-response'
            }
            self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            response = self.session.post('https://pb.nalog.ru/company-proc.json', data=data)
            return response.json(), None

    def check_nalog_step_2(self, token):
        self.session.get(f'https://pb.nalog.ru/company.html?token={token}')
        data = {
            'token': token,
            'method': 'get-request'
        }
        response = self.session.post('https://pb.nalog.ru/company-proc.json', data=data)
        if 'ERROR' in response.json():
            params = {
                'aver': '2.7.58',
                'sver': '4.38.63',
                'pageStyle': 'GM2'
            }
            response = self.session.get('https://pb.nalog.ru/captcha-dialog.html', params=params).text
            token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            params = {
                'a': token,
                'version': 2
            }
            img = self.session.get('https://pb.nalog.ru/static/captcha.bin', params=params)
            image_bytes = base64.b64encode(img.content)
            return None, image_bytes
        return response.json(), None

    def get_info(self, ex_id, token):
        data = {
            'token': token,
            'id': ex_id,
            'method': 'get-response'
        }
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        response = self.session.post('https://pb.nalog.ru/company-proc.json', data=data)
        return response.json()

    def get_pdf(self):
        params = {
            'query': self.inn,
            'page': 0
        }
        response = self.session.get('https://bo.nalog.ru/nbo/organizations/search', params=params)
        id_docs = response.json()['content'][0]['id']
        response = self.session.get(f'https://bo.nalog.ru/download/bfo/pdf/{id_docs}?period=2020')
        pdf_bytes = base64.b64encode(response.content)
        return pdf_bytes

    def check_inn(self):
        self.session.get('https://service.nalog.ru/bi.html')

        response = self.session.get(
            'https://service.nalog.ru/static/captcha-dialog.html?aver=3.40.10&sver=4.38.62&pageStyle=GM2'
        ).text
        token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
        params = {
            'a': token,
            'version': 2
        }
        img = self.session.get('https://service.nalog.ru/static/captcha.bin', params=params)
        image_bytes = base64.b64encode(img.content)
        return None, image_bytes, token

    def check_captcha_for_inn(self, captcha_value, captcha_token):
        self.session.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.71 Safari/537.36'
        }
        data = {
            'captcha': captcha_value,
            'captchaToken': captcha_token
        }
        response = self.session.post('https://service.nalog.ru/static/captcha-proc.json', data=data)
        if 'ERROR' in response.text:
            response = self.session.get(
                'https://service.nalog.ru/static/captcha-dialog.html?aver=3.40.10&sver=4.38.62&pageStyle=GM2'
            ).text
            token = re.findall(r'<input type="hidden" name="captchaToken" value="(.*)"/>', response)[0]
            params = {
                'a': token,
                'version': 2
            }
            img = self.session.get('https://service.nalog.ru/static/captcha.bin', params=params)
            image_bytes = base64.b64encode(img.content)
            return None, image_bytes, token
        else:
            token = re.findall(r'"(.*)"', response.text)[0]
            data = {
                'requestType': 'FINDPRS',
                'innPRS': self.inn,
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
            response = self.session.post('https://service.nalog.ru/bi2-proc.json', data=data).json()
            rows = response.get('rows')
            if rows:
                return rows, None, None
