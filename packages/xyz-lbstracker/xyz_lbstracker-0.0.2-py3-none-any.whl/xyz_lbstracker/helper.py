# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_util.crawlutils import http_get
from base64 import encodestring

def get_sina_short_url(url):
    r = http_get('https://sina.lt')
    bs = encodestring(url)
    r = http_get('https://sina.lt/api.php?from=w&url=%s&site=t.hk.uy' % bs, cookies = r.cookies)
    return r
