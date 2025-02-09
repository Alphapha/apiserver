# -*- coding: utf-8 -*-
# @Time : 2025/2/6 10:10
# @Auther : Char1es
# @Title : mysql_operate

from flask import Blueprint, request, jsonify
import pymysql
import os
from dotenv import load_dotenv
import sys
import re


load_dotenv()
mysql_operate_api = Blueprint('mysql_operate_api_', __name__)

mysql_host = os.getenv('mysql_host')
mysql_user = os.getenv('mysql_user')
mysql_password = os.getenv('mysql_password')
mysql_port = int(os.getenv('mysql_port'))


def is_valid(txt):
    """验证数据库名是否合法"""
    # 定义正则表达式模式，允许大小写字母数字和下划线
    txt_pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(txt_pattern, txt))


def create_database(dbname):
    if dbname is not None:
        if not is_valid(dbname):
            print(f"Invalid database name: {dbname}", file=sys.stderr)
            return
        with pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port,
                             charset='utf8mb4') as conn:
            try:
                # 创建一个游标对象
                cursor = conn.cursor()
                # 创建数据库的SQL命令
                create_db_query = f"CREATE DATABASE {dbname}"
                # 执行SQL命令
                cursor.execute(create_db_query)
                # 提交事务
                conn.commit()
                print(f"New database '{dbname}' created successfully.", file=sys.stderr)
                return {'status': 'success', 'message': f'create_database {dbname} successfully.'}
            except pymysql.MySQLError as e:
                print(f"Error occurred: {e}", file=sys.stderr)
                conn.rollback()
                return {'status': 'error', 'message': f'create_database {dbname} error! Error occurred: {e}'}
    else:
        print(f"create_database {dbname} error! dbname is Non", file=sys.stderr)
        return {'status': 'error', 'message': f'create_database {dbname} error! dbname is None'}


def create_table(dbname, tbname, **kwargs):
    if not is_valid(dbname):
        print(f"Invalid database name: {dbname}", file=sys.stderr)
        return
    if not is_valid(tbname):
        print(f"Invalid table name: {tbname}", file=sys.stderr)
        return
    str = ''
    for key, value in kwargs.items():
        str += ''.join(f'{key} {value},')
    str = str.rsplit(',', 1)[0]

    with pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                         port=mysql_port,
                         charset='utf8mb4', db=dbname) as conn:
        try:
            cursor = conn.cursor()
            sql = f'''
                CREATE TABLE {tbname}(
                    {str}
                );
            '''
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print(f"New table '{tbname}' created successfully.", file=sys.stderr)
            return {'status': 'success', 'message': f'create_table "{tbname}" successfully.'}
        except pymysql.MySQLError as e:
            print(f'Error occurred: {e}', file=sys.stderr)
            conn.rollback()
            return {'status': 'error', 'message': f'create_table "{tbname}" error! Error occurred: {e}'}


def insert_data(dbname, tbname, **kwargs):
    pass

def update_data(dbname, tbname, **kwargs):
    pass

def delete_data(dbname, tbname, **kwargs):
    pass

def search_data(dbname, tbname, **kwargs):
    pass


def execute_sql(dbname, sql):
    with pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                         port=mysql_port,
                         charset='utf8mb4', db=dbname) as conn:
        try:
            # 创建一个游标对象
            cursor = conn.cursor()

            # 执行SQL命令
            cursor.execute(sql)

            # 提交事务
            conn.commit()
            return {'status': 'success', 'message': f'executed_sql  successfully.'}
        except pymysql.MySQLError as e:
            print(f"Error occurred: {e}")
            return {'status': 'error', 'message': f'executed_sql error! Error occurred: {e}'}


# @mysql_operate_api.route('/createdb', methods=['POST'])
# def create_database_api___():
#     data = request.get_json()
#     dbname = data.get('dbname', 'python')
#     result = create_database(dbname=dbname)
#     return jsonify(result)

@mysql_operate_api.route('/createdb', methods=['GET'])
def create_database_api():
    # 从URL查询参数中获取dbname
    dbname = request.args.get('dbname', None)
    result = create_database(dbname=dbname)
    return jsonify(result)


@mysql_operate_api.route('/createtb', methods=['POST'])
def create_table_api___():
    data = request.get_json()
    dbname = data.get('dbname', 'python')
    tbname = data.get('tbname', 'python')
    data.pop('dbname', None)
    data.pop('tbname', None)
    result = create_table(dbname=dbname, tbname=tbname, **data)
    return jsonify(result)


@mysql_operate_api.route('/executesql', methods=['POST'])
def execute_sql_api___():
    data = request.get_json()
    dbname = data.get('dbname', 'python')
    sql = data.get('sql', None)
    result = execute_sql(dbname=dbname, sql=sql)
    return jsonify(result)