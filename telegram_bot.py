# 从 tgbot_funcs.py 导入定义机器人动作的函数
from multiprocessing import Queue

from configure import config, threads
import log_config
import service
import telebot
import controller

if __name__ == '__main__':

    # log_queue = Queue()
    log_config.init()
    controller.init()
    if config.start_tele_bot:
        telebot.init()
    service.init()

    for thread in threads:
        thread.join()
