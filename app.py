import logging
import os
from logging import handlers

BASE_URL = 'http://user-p2p-test.itheima.net'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_HOST = "52.83.144.39"
DB_USER = "root"
DB_PASSWORD = "Itcast_p2p_20191228"
MEMBER_DATABASE = 'czbk_member'
port = 3306
phone = "13017172525"
phone1 = "13017172526"
phone2 = "13017172527"
phone3 = "13017172528"
phone4 = '13017172529'
tender_id = 1129
imgCode = '8888'

# 定义日志初始化器
def init_log_config():
    # 创建日志器
    logger = logging.getLogger()
    # 日志级别的设置
    logger.setLevel(logging.INFO)
    # 创建控制台处理器和文件处理器
    sh = logging.StreamHandler()
    #file_name = "./" + "log.log"
    file_name = BASE_DIR + os.sep + "log" + os.sep + "log.log"
    fh = logging.handlers.TimedRotatingFileHandler(file_name,when='M',interval=2,backupCount=5)

    # 创建格式化器
    f = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(f)

    # 将格式化器添加到处理器
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 将控制器处理器和文件处理器绑定到日志器
    logger.addHandler(sh)
    logger.addHandler(fh)