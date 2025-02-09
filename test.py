import requests
import json
import argparse


def test(tbname):
    if tbname is None:
        tbname = 'CNYMYR'
    dbname = 'huilv'
    url_db = f"http://127.0.0.1:50001/mysql/createdb?dbname={dbname}"
    url_tb = "http://127.0.0.1:50001/mysql/executesql"
    create_tb_sql = f"""
    CREATE TABLE {tbname} (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        timestamp BIGINT UNIQUE,
        time DATE NOT NULL,
        open_price DECIMAL(10, 6) NOT NULL,
        close_price DECIMAL(10, 6) NOT NULL,
        high_price DECIMAL(10, 6) NOT NULL,
        low_price DECIMAL(10, 6) NOT NULL,
        range_price DECIMAL(10, 6) NOT NULL,
        ratio DECIMAL(7, 4) NOT NULL,
        ma5_avg_price DECIMAL(10, 6),
        ma10_avg_price DECIMAL(10, 6),
        ma20_avg_price DECIMAL(10, 6),
        insert_time DATE NOT NULL DEFAULT (CURRENT_DATE)
    );
    """
    data = json.dumps({"dbname": dbname, "sql": create_tb_sql})

    headers = {
      'Content-Type': 'application/json'
    }
    # 数据库创建
    create_db = requests.get(url_db).json()
    print(f'create_db results: {create_db}')
    # 表创建
    create_tb = requests.post(url_tb, data=data, headers=headers).json()
    print(f'create_tb results: {create_tb}')

    # 汇率查询
    url = "http://127.0.0.1:50001/exchange_rate"
    payload = json.dumps({
      "exchangetype": f"{tbname}",
      "ktype": "day"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.json().get("Result", {}).get("newMarketData", {}).get("marketData", None) is not None:
        marketData = response.json().get("Result", {}).get("newMarketData", {}).get("marketData", None)
        str = ''
        for i in marketData.split(';'):
            # 1251648000,2009-08-31,13.862300,13.626300,14.312100,13.544600,-0.2272,-1.6400,13.9977,13.9129,14.4911
            parts = i.split(',')
            parts[1] = f"'{parts[1]}'"
            new_i = f"({','.join(parts)}),"
            # (1251648000,'2009-08-31',13.862300,13.626300,14.312100,13.544600,-0.2272,-1.6400,13.9977,13.9129,14.4911),
            str += ''.join(new_i)
        str_new = str.rsplit(',', 1)[0]+';'
        sql = f"""
            INSERT IGNORE INTO {tbname} (timestamp, time, open_price, close_price, high_price, low_price, range_price, ratio, ma5_avg_price, ma10_avg_price, ma20_avg_price) VALUES{str_new}
        """
        insert_data = json.dumps({"dbname": dbname, "sql": sql})
        # print(insert_data)

        # 汇率查询结果存入数据库
        insert = requests.post(url_tb, data=insert_data, headers=headers).json()
        print(f'insert_data results: {insert}')
        #print(f'{dbname} updated!')
        # print(str_new)

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="请输入需要查询的货币对，例：CNYMYR means 人民币兑马来币")
    # 添加-p/--param参数
    par.add_argument('-p', '--param', type=str, required=True,
                        help='请输入需要查询的货币对，例：CNYMYR means 人民币兑马来币')
    args = par.parse_args()
    test(args.param)
