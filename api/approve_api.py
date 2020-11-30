import app


class ApproveAPI(object):
    # 初始化方法
    def __init__(self):
        self.approve_url = app.BASE_URL + "/member/realname/approverealname"

    # 认证接口方法
    def approve(self,session,realname,cardId):
        # 1、准备请求的参数数据
        data = {"realname": realname, "card_id": cardId}
        # 2、发送请求、接收响应
        response = session.post(self.approve_url,data=data,files={'x':'y'})
        # 3、 返回响应
        return response