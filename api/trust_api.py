import app


class TrustAPI(object):
    # 初始化方法
    def __init__(self):
        self.trust_register_url = app.BASE_URL + "/trust/trust/register"
        self.get_recharge_code_url = app.BASE_URL + "/common/public/verifycode/"
        self.recharge_url = app.BASE_URL + "/trust/trust/recharge"

    # 定义开户的请求接口
    def trust_register(self,session):
        # 准备参数
        # 发送请求，接收响应
        response = session.post(self.trust_register_url)
        # 返回响应
        return response

    # 定义获取充值验证码的接口
    def get_recharge_code(self,sesion,r):
        # 准备参数
        url = self.get_recharge_code_url + r
        # 发送请求，并接收响应
        response = sesion.get(url)
        # 返回响应
        return response

    # 定义充值的接口
    def recharge(self,session,amount,paymentType="chinapnrTrust",formStr="reForm",valicode="8888"):
        # 准备参数
        data = {"paymentType": paymentType,
                "formStr": formStr,
                "amount": amount,
                "valicode": valicode}
        # 发送请求，并接收响应
        response = session.post(self.recharge_url,data=data)
        # 返回响应
        return response