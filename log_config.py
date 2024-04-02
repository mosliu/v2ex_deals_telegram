# 加载预处理

import logging.config
import json
import os
import sys
from multiprocessing import Queue

log_queue = Queue()

def config_logging():
    if not os.path.exists('config/logging_config.json'):
        sys.exit("no configs file")
    with open('config/logging_config.json', 'r') as f:
        logging_config = json.load(f)

    logging.config.dictConfig(logging_config)


# with open('config/logging_config.json', 'r') as f:
#     logging_config = json.load(f)
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

def init():
    config_logging()

