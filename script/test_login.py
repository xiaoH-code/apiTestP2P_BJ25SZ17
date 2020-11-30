import logging
import time
import unittest
from api.login_api import LoginAPI
import requests
import random
import app
from utils import assert_utils,DButils

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sql1 = "delete i.* from mb_member_info i inner join mb_member m on i.member_id = m.id where m.phone in ({},{},{},{},{});"
        DButils.execute_sql(sql1.format(app.phone,app.phone1,app.phone2,app.phone3,app.phone4))
        logging.info("sql1 = {}".format(sql1.format(app.phone,app.phone1,app.phone2,app.phone3,app.phone4)))
        sql2 = "delete l.* from mb_member_login_log l inner join mb_member m on l.member_id = m.id where m.phone in ({},{},{},{},{});"
        DButils.execute_sql(sql2.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4))
        logging.info("sql2 = {}".format(sql2.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4)))
        sql3 = "delete from mb_member where phone in ({},{},{},{},{});"
        DButils.execute_sql(sql3.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4))
        logging.info("sql3 = {}".format(sql3.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4)))
        sql4 = "delete from mb_member_register_log where phone in ({},{},{},{},{});"
        DButils.execute_sql(sql4.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4))
        logging.info("sql4 = {}".format(sql4.format(app.phone, app.phone1, app.phone2, app.phone3, app.phone4)))

    # 前置脚本
    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.session = requests.Session()

    # 后置脚本
    def tearDown(self) -> None:
        self.session.close()

    # 随机小数获取图片验证码成功
    def test01_get_img_code_success_random_float(self):
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

    # 随机整数获取图片验证码成功
    def test02_get_img_code_success_random_int(self):
        # 准备测试数据
        r_data = random.randint(1000000,9999999)
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info("response = {}".format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

    # 参数为空，获取图片验证码失败
    def test03_get_img_code_fail_param_is_null(self):
        # 准备测试数据
        r_data = ""
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_img_verify_code(self.session,r_data)
        logging.info("response = {}".format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(404,response.status_code)

    # 参数为字母，获取图片验证码失败
    def test04_get_img_code_fail_param_is_char(self):
        # 准备测试数据
        r_list = random.sample("abcdefghijklmn",8)
        # 列表拼接为字符串
        r_data = "".join(r_list)
        logging.info("r_data = {}".format(r_data))
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_img_verify_code(self.session,r_data)
        # 对返回的响应内容进行断言
        self.assertEqual(400,response.status_code)

    # 参数正确时，获取短信验证码成功
    def test05_get_sms_code_success_param_is_true(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        # response = self.login_api.get_sms_verify_code(self.session,TestLogin.phone,TestLogin.imgCode)  # 使用类属性来定义参数
        response = self.login_api.get_sms_verify_code(self.session, app.phone, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # self.assertEqual(200,response.status_code)
        # self.assertEqual(200,response.json().get("status"))
        # self.assertEqual("短信发送成功",response.json().get("description"))

    # 图片验证错误，获取短信验证码失败
    def test06_get_sms_code_fail_img_code_is_wrong(self):
        # 1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        wrong_code = '1234'
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone,wrong_code)
        logging.info("response = {}".format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 图片验证码为空，获取短信验证码失败
    def test07_get_sms_code_fail_img_code_is_null(self):
        # 1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        imgCode = ""
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone,imgCode)
        logging.info("response = {}".format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 图片手机号为空，获取短信验证码失败
    def test08_get_sms_code_fail_phone_is_null(self):
        # 1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        phone = ""
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session,phone,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    def test09_get_sms_code_fail_no_img_code(self):
        # 1、获取图片验证码
        # 2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 输入必填项，注册成功
    def test10_register_success_param_is_must(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口的方法
        response = self.login_api.register(self.session,app.phone)
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"注册成功")

    # 输入所有参数项，注册成功
    def test11_register_success_all_params(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone1, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用封装API接口的方法
        response = self.login_api.register(self.session,app.phone1,invitePhone="13012345678")
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应该内容进行断言
        assert_utils(self,response,200,200,"注册成功")

    # 手机号已存在时，注册失败
    def test12_register_fail_phone_is_exist(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone1, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用API接口的方法
        response = self.login_api.register(self.session,app.phone1)
        logging.info('response = {}'.format(response.json()))
        # 对应响应进行断言
        assert_utils(self,response,200,100,"手机已存在!")

    # 密码为空，注册失败
    def test13_register_fail_pwd_is_null(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone2, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        response = self.login_api.register(self.session,app.phone2,pwd="")
        logging.info('response = {}'.format(response.json()))
        # 调用API接口的方法
        assert_utils(self,response,200,100,"密码不能为空")

    def test14_register_fail_img_code_is_wrong(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone3, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用API接口方法
        response = self.login_api.register(self.session,app.phone3,imgCode='1234')
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,100,"验证码错误!")

    # 短信验证码错误，注册失败
    def test15_register_fail_sms_code_is_wrong(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone3, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用API接口方法
        response = self.login_api.register(self.session,app.phone3,phoneCode="123456")
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,100,"验证码错误")

    # 不同意协议，注册失败
    def test16_register_fail_no_agree_protocol(self):
        #1、获取图片验证码
        # 准备测试数据
        r_data = random.random()
        # 调用封装API接口，传入测试数据，接收API接口返回的响应
        response = self.login_api.get_img_verify_code(self.session,str(r_data))
        logging.info('response = {}'.format(response.text))
        # 对返回的响应内容进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 准备测试数据
        # 调用封装API接口，传入测试数据，接收API接口放回的响应
        response = self.login_api.get_sms_verify_code(self.session, app.phone3, app.imgCode)  # 使用app定义全局参数（变量）
        logging.info('response = {}'.format(response.json()))
        # 对返回的响应内容进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用API接口方法
        response =self.login_api.register(self.session,app.phone3,dyServer="off")
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,100,"请同意我们的条款")

    # 正确输入用户名密码，登录成功
    def test17_login_success(self):
        # 准备测试数据
        # 调用API接口方法
        response = self.login_api.login(self.session,app.phone)
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 用户不存在时，登录失败
    def test18_login_fail_phone_is_null(self):
        # 准备测试数据
        # 调用API接口方法
        response = self.login_api.login(self.session,"")
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,100,"用户名不能为空")

    # 密码为空时，登录失败
    def test19_login_fail_pwd_is_null(self):
        # 准备测试数据
        # 调用API接口方法
        response = self.login_api.login(self.session,app.phone,"")
        logging.info('response = {}'.format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    # 密码错误时，登录失败
    def test20_login_fail_pwd_is_wrong(self):
        wrong_pwd = "error"
        # 1、密码错误1次，给出提示
        response = self.login_api.login(self.session,app.phone,wrong_pwd)
        logging.info("first response = {}".format(response.json()))
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        # 2、密码错误2次，给出提示
        response = self.login_api.login(self.session,app.phone,wrong_pwd)
        logging.info("secode response = {}".format(response.json()))
        assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")
        # 3、密码错误3次，被锁定
        response = self.login_api.login(self.session,app.phone,wrong_pwd)
        logging.info("third response = {}".format(response.json()))
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 4、锁定后1分钟内重新输入正确密码，提示锁定
        response = self.login_api.login(self.session,app.phone)
        logging.info("forth response = {}".format(response.json()))
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 5、锁定后1分钟后重新输入正确密码，登录成功
        time.sleep(60)
        response = self.login_api.login(self.session,app.phone)
        logging.info("five response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")