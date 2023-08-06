import requests
from bs4 import BeautifulSoup

import json
from datetime import datetime
import hmac
import base64
import uuid

class Translator(object):

    # headers 보안키 생성
    def hmac_md5(self, key, s):
        return base64.b64encode(hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').digest()).decode()


    def translate(self, data, get_all_data=False):
        # input = 번역할 영어 String
        # output = 번역 된 String

        url = 'https://papago.naver.com/apis/n2mt/translate'

        # papago version (안맞으면 오류발생)
        AUTH_KEY = 'v1.6.4_4b23b99383'


        dt = datetime.now()
        timestamp = str(round(dt.timestamp()*1000))

        # 고정 값을 사용할 시 서버로 부터 차단을 방지
        deviceId = str(uuid.uuid4())

        hmac = self.hmac_md5(AUTH_KEY, deviceId + '\n' + url + '\n' + timestamp)

        headers = {
                    'authorization': 'PPG ' + deviceId + ':' + hmac,
                    'timestamp': timestamp
                    }

        form_data = {
                    'deviceId': deviceId,
                    'locale': 'ko',
                    'dict': 'true',
                    'dictDisplay': 30,
                    'honorific': 'false',
                    'instant': 'false',
                    'paging': 'false',
                    'source': 'en',
                    'target': 'ko',
                    'text': data.lower()
                    }
        res_data = requests.post(url, data=form_data, headers=headers)

        if get_all_data == True:
            print(json.dumps(res_data.json(), indent='\t', ensure_ascii=False))
        
        return res_data.json()['translatedText']


    # 영어 list -> 한국어 list
    def en_list_to_ko_list(self, en_list):
        ko_list = []
        for text in en_list:
            ko_list.append(self.translate(text))

        return ko_list
