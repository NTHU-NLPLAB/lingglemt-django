#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
from urllib.request import urlopen
from urllib.parse import quote

'''Return the translation using google translate
you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
if you don't define anything it will detect it or use english by default
Example:
print(translate("salut tu vas bien?", "en"))
hello you alright?'''

gtrans_url = 'http://translate.google.com/m?hl=%s&sl=%s&q=%s'
before_trans = 'class="t0">'
_user_agent = (
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; '
    '.NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'
)
_headers = {
    'User-Agent': _user_agent
}


def gtrans(to_translate, trg="zh-TW", src="en"):
    link = gtrans_url % (trg, src, quote(to_translate))
    request = urllib.request.Request(link, headers=_headers)
    page = urlopen(request).read().decode('utf-8')

    result = page[page.find(before_trans) + len(before_trans):]
    result = result.split('<', 1)[0]

    return result

if __name__ == '__main__':
    sents = ['harmful to environment', 'harmful to brain', 'leave from Seattle']

    for sent in sents:
        print(sent, '==>', gtrans(sent))
