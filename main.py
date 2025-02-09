# -*- coding: utf-8 -*-
# @Time : 2025/2/5 23:06
# @Auther : Char1es
# @Title : main


from flask import Flask
from api.get_exchange_rate import exchange_rate_api
from api.mysql_operate import mysql_operate_api
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

# 注册蓝图
app.register_blueprint(exchange_rate_api, url_prefix='/exchange_rate')
app.register_blueprint(mysql_operate_api, url_prefix='/mysql')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50001)

