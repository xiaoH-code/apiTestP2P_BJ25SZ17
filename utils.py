# 对返回的响应内容进行断言
import json
import logging

import pymysql
from bs4 import BeautifulSoup
import requests

import app


def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

# 封装第三方的请求的参数提取及请求发送的方法
def third_part_request(html_data):
    # 提取响应的HTML数据中的内容
    soup = BeautifulSoup(html_data, "html.parser")
    # 提取请求的url
    request_url = soup.form['action']
    # 提取请求的参数值
    data = {}
    for s in soup.find_all('input'):
        data.setdefault(s['name'], s['value'])
    logging.info("data = {}".format(data))
    # 发送请求并接收响应
    response = requests.post(request_url, data=data)
    logging.info("third-part response = {}".format(response.text))
    return response

class DButils(object):
    @classmethod
    def get_conn(cls):
        cls.conn = pymysql.connect(host=app.DB_HOST,user=app.DB_USER,password=app.DB_PASSWORD,database=app.MEMBER_DATABASE,port=3306,autocommit=True)
        return cls.conn

    @classmethod
    def close_conn(cls,cursor,conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def execute_sql(cls,sql):
        try:
            conn = cls.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cls.close_conn(cursor,conn)


# 提取获取图片验证码的参数化文件中的测试数据
def get_img_verify_code_data():
    # 获取文件路径
    file_path = app.BASE_DIR + "/data/img_verify_code.json"
    test_case_list = []
    # 打开文件并读取内容
    with open(file_path) as f:
        #将json文件转化为字典格式的文件
        json_data = json.load(f)
        #获取定义的测试数据
        test_data = json_data.get("get_img_verify_code")
        #循环读取参数文件中定义的每一组测试数据
        for case_data in test_data:
            test_case_list.append((case_data.get("type"),case_data.get("status_code")))
    # 返回列表（列表中的每一个值是元组/列表）
    print(test_case_list)
    return test_case_list

# 提取注册的参数化文件中的测试数据
def get_register_data():
    # 1、获取参数化文件路径
    file_path = app.BASE_DIR + "/data/register.json"
    test_case_list = []
    # 2、 打开文件并读取内容
    with open(file_path,encoding="utf-8") as f:
        #将JSON文件转化为字典格式的文件
        json_data = json.load(f)
        #获取定义的测试数据
        test_data = json_data.get("test_register")
        # 循环读取参数文件中定义的每一组测试数据
        for case_data in test_data:
            test_case_list.append((case_data.get("phone"),case_data.get("pwd"),case_data.get("imgCode"),case_data.get("phoneCode"),case_data.get("dyServer"),case_data.get("invitePhone"),case_data.get("status_code"),case_data.get("status"),case_data.get("description")))
    # 3、 返回数据列表（列表中每一个值都是元组或者列表）
    print(test_case_list)
    return test_case_list


# 定义一个读取参数化数据文件的函数
def read_param_data(file_name,method_name,params):
    """
    :param file_name: 需要读取的参数化文件的文件名称。例如：register.json
    :param method_name: 需要读取的参数化文件中定义的方法名（也就是测试数据列表值对应的键名）。例如：test_register
    :param params:  由参数化文件中的所有参数名组成的字符串，以","为分隔。例如："phone,pwd,imgCode,phoneCode,dyServer,invitePhone,status_code,status,desc"
    :return: 返回数据列表（列表中每一个值都是元组或者列表）
    """
    # 获取文件路径
    file_path = app.BASE_DIR + "/data/" + file_name
    test_case_list = []
    # 打开文件并读取内容
    with open(file_path,encoding="utf-8") as f:
        # 将JSON文件转化为字典格式的文件
        json_data = json.load(f)
        # 获取定义的测试数据
        test_data = json_data.get(method_name)
        # 循环读取参数文件中定义的每一组测试数据
        for case_data in test_data:
            test_case_data = []
            # 针对每一组测试数据，循环读取每一个参数的值，并组成一个列表
            for param in params.split(','):
                test_case_data.append(case_data[param])
            # 将一组参数值的列表数据 test_case_data ，添加到返回的列表中
            test_case_list.append(test_case_data)
    # 返回列表
    print(test_case_list)
    return test_case_list