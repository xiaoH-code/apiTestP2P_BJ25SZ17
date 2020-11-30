from app import init_log_config
import logging

init_log_config()
logging.error('error')
logging.info('info')
logging.debug('debug')