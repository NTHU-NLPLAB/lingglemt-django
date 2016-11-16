#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
import json

BING_TRANS_URL = 'http://www.bing.com/translator/'
API_URL = 'api/Translate/TranslateArray?from=%s&to=%s'
BATCH_SIZE = 200


class BingTranslator:

    def __init__(self):
        r = requests.get(BING_TRANS_URL)
        # self.__session = requests.Session()
        # r = self.__session.get(BING_TRANS_URL)
        self.__header = {
            # 'Cookie': 'MUID=%(MUID)s; mtstkn=%(mtstkn)s;' % r.cookies,
            'Cookie': 'MUID={MUID}; mtstkn={mtstkn};'.format(**r.cookies),
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def __on_session_expire__(self):
        self.__init__()

    def __translate__(self, data, fromlang='en', tolang='zh-CHT'):
        url = urljoin(BING_TRANS_URL, API_URL % (fromlang, tolang))
        data = json.dumps(data)

        result = None
        for _ in range(5):
            response = requests.post(url, headers=self.__header, data=data)
            # response = self.__session.post(url, cookies=self.__session.cookies, data=data)
            result = response.json()
            if response.status_code == 200 and 'items' in result:
                return [item['text'] for item in result['items']]
            else:
                self.__on_session_expire__()

    def translate_one(self, sent):
        data = [{'text': sent}]
        res = self.__translate__(data)[0]
        return res

    def translate_many(self, sents):
        res = []
        data = [{'text': sent} for sent in sents]
        for i in range(0, len(data), BATCH_SIZE):
            res += self.__translate__(data[i:i + BATCH_SIZE])
        return res


if __name__ == '__main__':
    translator = BingTranslator()
    sents = ['harmful to environment', 'harmful to brain', 'leave from Seattle']

    # example of translating one sentence at a time
    # for sent in sents:
    #     print '%s ==> %s' % (sent, translator.translate_one(sent))

    # example of translating many sentences at the same time
    res = translator.translate_many(sents)
    print(res)
    for en, zh in zip(sents, res):
        print(en, '==>', zh)
