import logging

from multiprocessing import Process
from flask import Flask, request
from configure import config, threads
from loguru import logger

from log_config import InterceptHandler

app = Flask(__name__)


# def setup_loguru(app,log_level='WARNING'):
#     logger.add(
#         'logs/{time:%Y-%m-%d}.log',
#         level='DEBUG',
#         format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
#         backtrace=False,
#         rotation='00:00',
#         retention='20 days',
#         encoding='utf-8'
#     )
#
#     app.logger.addHandler(InterceptHandler())
#     logging.basicConfig(handlers=[InterceptHandler()], level=log_level)

# def init_log(log_queue):
#     qh = logging.handlers.QueueHandler(log_queue)
#     global logger
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(qh)


def init():
    logger.info("start initializing controller...")
    # app.logger.addHandler(InterceptHandler())
    # logging.basicConfig(handlers=[InterceptHandler()], level="DEBUG")
    # logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    ip = config.listen_ip
    port = config.listen_port
    is_pro = config.is_production
    if ip is None:
        ip = '0.0.0.0'
    if port is None:
        port = 8744
    if is_pro is None:
        is_pro = True
    p = Process(target=start_server, args=(ip, port, is_pro))
    p.deamon = True
    # 启动Flask应用
    p.start()
    threads.append(p)


def start_server(ip, port, is_pro):
    logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)
    if is_pro:
        # 创建Process对象
        # p = Process(target=app.run(host=ip, port=port, threaded=True))
        # p.deamon = True
        # # 启动Flask应用
        # p.start()
        # threads.append(p)
        # # 等待Flask应用运行
        # # p.join()
        logger.info("start controller in pro mode")
        app.run(host=ip, port=port, threaded=True)
    else:
        logger.info("start controller in debug mode")
        app.run(debug=True, host=ip, port=port, threaded=True)
        # # 创建Process对象
        # p = Process(target=app.run(debug=True, host=ip, port=port, threaded=True))
        # p.deamon = True
        # # 启动Flask应用
        # p.start()
        # threads.append(p)
        # # 等待Flask应用运行
        # # p.join()
        # # app.run(host=ip, port=port, threaded=True)


from . import index_controller
