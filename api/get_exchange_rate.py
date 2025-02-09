# -*- coding: utf-8 -*-
# @Time : 2025/2/5 23:24
# @Auther : Char1es
# @Title : get_exchange_rate

from flask import Blueprint, request, jsonify
import requests


exchange_rate_api = Blueprint('get_exchange_rate_api', __name__)

hearder = {"Accept": "*/*",
               #"Access-Control-Request-Method": "GET",
               #"Access-Control-Request-Headers": "acs-token",
               #"Origin": "https://gushitong.baidu.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6285.209 Safari/537.36",
               #"Sec-Fetch-Mode": "cors",
               #"Sec-Fetch-Site": "same-site",
               #"Sec-Fetch-Dest": "empty",
               #"Referer": "https://gushitong.baidu.com/",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
               "Sec-Ch-Ua-Platform": "\"Windows\"",
               "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"125\", \"Google Chrome\";v=\"125\"",
               "Sec-Ch-Ua-Mobile": "?0",
               "Priority": "u=1, i"
}


def get_exchange_rate(exchangetype=None, ktype=None):
    if exchangetype is None:
        exchangetype = 'CNYJPY'
    if ktype is None:
        ktype = 'day'

    # 百度股市通接口
    url = f'https://finance.pae.baidu.com/vapi/v1/getquotation?group=huilv_kline&ktype={ktype}&code={exchangetype}&finClientType=pc'
    try:
        #print(url)
        resp = requests.request("get", url=url, headers=hearder)
        #print(resp.text)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return {"Error": str(e)}


def get_exchange_rate_real(exchangetype=None):
    if exchangetype is None:
        exchangetype = 'CNYJPY'
    url = f'https://finance.pae.baidu.com:443/vapi/v1/getquotation?group=huilv_minute&need_reverse_real=1&code={exchangetype}&finClientType=pc'
    resp = requests.options(url=url, headers=hearder)
    print(resp.text)
    try:
        prices = {item['name']: item['value'] for item in resp.json()['Result']['pankouinfos']['list']}
        print(f'今天{exchangetype}汇率为：{prices}') # {'今开': '0.6122', '最高': '0.6130', '买入价': '0.6069', '昨收': '0.6129', '最低': '0.6069', '卖出价': '0.6084'}
        # open = prices.get('今开', 'N/A')
        # preClose = prices.get('昨收', 'N/A')
        # high = prices.get('最高', 'N/A')
        # low = prices.get('最低', 'N/A')
        # bid_grp = prices.get('买入价', 'N/A')
        # offer_grp = prices.get('卖出价', 'N/A')
        return prices
    except requests.exceptions.RequestException as e:
        #print(f'Error: {e}')
        return {"Error": str(e)}

@exchange_rate_api.route('/', methods=['POST'])
def exchange_api():
    data = request.get_json()
    exchangetype = data.get('exchangetype', 'CNYJPY')
    ktype = data.get('ktype', 'day')
    result = get_exchange_rate(exchangetype=exchangetype, ktype=ktype)
    return jsonify(result)


@exchange_rate_api.route('/real', methods=['GET'])
def exchange_api_real():
    exchangetype = request.args.get('exchangetype', 'CNYJPY')
    result = get_exchange_rate_real(exchangetype=exchangetype)
    return jsonify(result)
