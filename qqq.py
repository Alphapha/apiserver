# -*- coding: utf-8 -*-
# @Time : 2025/2/5 23:52
# @Auther : Char1es
# @Title : qqq


import requests


def get_exchange_rate(exchangetype=None):
    if exchangetype is None:
        exchangetype = 'CNYJPY'
    hearder = {"Accept": "*/*",
               "Access-Control-Request-Method": "GET",
               "Access-Control-Request-Headers": "acs-token",
               "Origin": "https://gushitong.baidu.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6285.209 Safari/537.36",
               "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Site": "same-site",
               "Sec-Fetch-Dest": "empty",
               "Referer": "https://gushitong.baidu.com/",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
               "Sec-Ch-Ua-Platform": "\"Windows\"",
               "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"125\", \"Google Chrome\";v=\"125\"",
               "Sec-Ch-Ua-Mobile": "?0",
               "X-Forwarded-For": "144.144.144.144",
               "X-Originating-Ip": "144.144.144.144",
               "X-Remote-Ip": "144.144.144.144",
               "X-Remote-Addr": "144.144.144.144",
               "Priority": "u=1, i"}
    url = f'https://finance.pae.baidu.com/vapi/v1/getquotation?group=huilv_kline&ktype=month&code={exchangetype}&finClientType=pc'
    print(url)
    resp = requests.options(url, headers=hearder)
    print(resp.text)

if __name__ == '__main__':
    get_exchange_rate()