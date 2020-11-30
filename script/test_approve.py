import logging
import unittest
import requests

import app
from api.approve_api import ApproveAPI
from api.login_api import LoginAPI
from utils import assert_utils


class TestApprove(unittest.TestCase):
    realname = "张三"
    card_id = "110117199003070995"

    # 前置方法
    def setUp(self) -> None:
        # 接口对象与session对象的初始化
        self.approve_api = ApproveAPI()
        self.session = requests.Session()
        self.login_api = LoginAPI()

    # 后置方法
    def tearDown(self) -> None:
        self.session.close()

    # 测试用例脚本
    # 实名认证成功
    def test01_approve_success(self):
        #1、登录
        response = self.login_api.login(self.session,app.phone)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #2、认证请求成功
        #准备测试数据
        #调用API接口方法
        response = self.approve_api.approve(self.session,TestApprove.realname,TestApprove.card_id) #使用类属性
        logging.info("approve response = {}".format(response.json()))
        #对响应结果进行断言
        assert_utils(self,response,200,200,"提交成功!")

    # 姓名为空，实名认证失败
    def test02_approve_fail_name_is_null(self):
        #1、登录
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #2、认证请求成功
        #准备测试数据
        #调用API接口方法
        response = self.approve_api.approve(self.session,"",TestApprove.card_id)
        logging.info("approve response = {}".format(response.json()))
        #对响应结果进行断言
        assert_utils(self,response,200,100,"姓名不能为空")

    # 身份证号为空，实名认证失败
    def test03_approve_fail_cardId_is_null(self):
        #1、登录
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #2、认证请求成功
        #准备测试数据
        #调用API接口方法
        response = self.approve_api.approve(self.session,TestApprove.realname,"")
        logging.info("approve response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"身份证号不能为空")