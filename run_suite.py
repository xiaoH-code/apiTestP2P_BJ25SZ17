import time
import unittest

from script.tender import tender
from script.tender_process import test_tender_process
from script.test_approve import TestApprove
from script.test_login_params import TestLogin
from script.test_trust import TestTrust
import app
from lib.HTMLTestRunner_PY3 import HTMLTestRunner

# 创建测试套件对象
suite = unittest.TestSuite()

# 将所有测试脚本添加到测试套件
#suite.addTest(unittest.makeSuite(TestLogin))
suite.addTest(unittest.makeSuite(TestLogin))
suite.addTest(unittest.makeSuite(TestApprove))
suite.addTest(unittest.makeSuite(TestTrust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(test_tender_process))

#report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d_%H%M%S"))
report_file = app.BASE_DIR + "/report/report.html"
# 运行套件，并将运行结果写入到测试报告
with open(report_file,'wb') as f:
    runner = HTMLTestRunner(f,title='金融项目接口自动化测试报告',description="v1.0")
    runner.run(suite)
