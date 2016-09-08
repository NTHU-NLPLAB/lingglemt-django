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
            'Cookie': 'MUID=%(MUID)s; mtstkn=%(mtstkn)s;' % r.cookies,
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def __on_session_expire__(self):
        self.__init__()

    def __translate__(self, data, fromlang='en', tolang='zh-CHT'):
        url = urljoin(BING_TRANS_URL, API_URL % (fromlang, tolang))
        data = json.dumps(data)
        response = requests.post(url, headers=self.__header, data=data)
        # response = self.__session.post(url, cookies=self.__session.cookies, data=data)
        result = response.json()
        for i in range(3):
            if response.status_code == 200 and 'items' in result:
                for item in result['items']:
                    yield item['text']
            else:
                self.__on_session_expire__()

    def translate_one(self, sent):
        data = [{'text': sent}]
        res = next(self.__translate__(data))
        return res

    def translate_many(self, sents):
        res = []
        data = [{'text': sent} for sent in sents]
        for i in range(0, len(data), BATCH_SIZE):
            res += list(self.__translate__(data[i:i+BATCH_SIZE]))
        return res


if __name__ == '__main__':
    translator = BingTranslator()
    sents = ['harmful to environment', 'harmful to brain', 'leave from Seattle']

    # example of translating one sentence at a time
    # for sent in sents:
    #     print '%s ==> %s' % (sent, translator.translate_one(sent))

    # example of translating many sentences at the same time
    res = translator.translate_many(sents)
    for en, zh in zip(sents, res):
        print(en, '==>', zh)
