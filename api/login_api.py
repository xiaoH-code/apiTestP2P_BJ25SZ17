import app


class LoginAPI(object):
    # 完成数据初始化
    def __init__(self):
        self.img_verify_code_url = app.BASE_URL + "/common/public/verifycode1/"
        self.sms_verify_code_url = app.BASE_URL + "/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL + "/member/public/login"

    # 定义获取图片验证码的接口
    def get_img_verify_code(self, session, r):
        # 1、接收请求的参数
        url = self.img_verify_code_url + r
        # 2、发送请求，并接收响应
        response = session.get(url)
        # 3、返回响应
        return response

    # 定义获取短信验证码的接口
    def get_sms_verify_code(self, session, phone, imgCode):
        # 1、接收请求的参数
        data = {'phone': phone, 'imgVerifyCode': imgCode, 'type': 'reg'}
        # 2、发送请求，并接收响应
        response = session.post(self.sms_verify_code_url, data=data)
        # 3、返回响应
        return response

    # 定义注册的接口
    def register(self, session, phone, pwd="test123", imgCode="8888", phoneCode="666666", dyServer="on",
                 invitePhone=""):
        # 1、接收请求的参数
        data = {"phone": phone,
                "password": pwd,
                "verifycode": imgCode,
                "phone_code": phoneCode,
                "dy_server": dyServer,
                "invite_phone": invitePhone}
        # 2、发送请求，并接收响应
        response = session.post(self.register_url, data=data)
        # 3、返回响应
        return response

    # 定义登录的接口
    def login(self,session,keywords,pwd="test123"):
        #1、接收请求的参数
        data = {"keywords": keywords,"password": pwd}
        #2、发送请求，并接收响应
        response = session.post(self.login_url,data=data)
        #3、返回响应
        return response