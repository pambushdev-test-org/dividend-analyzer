import os
import logging
from logging.handlers import RotatingFileHandler
from . import config

# Setup project variables
configs 	= config.get_configs()
PARENT_DIR 	= os.path.abspath(os.path.dirname(__file__))
DATA_DIR 	= configs['DATA']['DATA_DIR']
DATA_SOURCE = configs['DATA']['DATA_SOURCE']
API_KEYS 	= configs['API_KEYS']
TICKER_LIST = configs['TICKERS']['TICKER_LIST']
EMAIL_VARS 	= configs['EMAIL_VARS']

# Setup logging config with rotating file handler
log_file = os.path.join(PARENT_DIR, 'logs/logs.txt')
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=2)
logging.basicConfig(encoding='utf-8',
					format='%(asctime)s %(message)s',
					datefmt='%Y/%m/%d/ %I:%M:%S %p', 
					level=logging.DEBUG,
					handlers=[handler])