# 加载预处理
import inspect
import logging.handlers

from itertools import chain
from types import FrameType
from typing import cast
import json
import os
import sys
import threading
# from configure import config, log_queue
from configure import config
from loguru import logger

folder_ = "./logs/"
prefix_ = "telebot_"
rotation_ = "50 MB"
retention_ = "30 days"
encoding_ = "utf-8"
backtrace_ = True
diagnose_ = True
# 格式里面添加了process和thread记录，方便查看多进程和线程程序
format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
          '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> ' \
          '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'


# from loguru_logging_intercept import InterceptHandler, setup_loguru_logging_intercept


# log_thread = None
# this_log_queue = None
#
#
# def logger_thread(log_queue):
#     """
#     单独的日志记录线程
#     """
#     while True:
#         record = log_queue.get()
#         if record is None:
#             break
#         # 获取record实例中的logger
#         logger = logging.getLogger(record.name)
#         # 调用logger的handle方法处理
#         logger.handle(record)


class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging module"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1
        logger_with_opts = logger.opt(depth=depth, exception=record.exc_info)
        config_logging(logger_with_opts)

        try:
            logger_with_opts.log(level, "{}", record.getMessage())
        except Exception as e:
            safe_msg = getattr(record, 'msg', None) or str(record)
            logger_with_opts.warning(
                "Exception logging the following native logger message: {}, {!r}",
                safe_msg,
                e
            )


def setup_loguru_logging_intercept(level=logging.DEBUG, modules=()):
    logging.basicConfig(handlers=[InterceptHandler()], level=level)  # noqa
    for logger_name in chain(("",), modules):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def config_logging(my_logger):
    # global logger

    my_logger.remove()
    # 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
    my_logger.add(sys.stdout, level="DEBUG", backtrace=backtrace_, diagnose=diagnose_,
                  format=format_, colorize=True)
    # basic
    my_logger.add(folder_ + prefix_ + "log.log", level="DEBUG", backtrace=backtrace_, diagnose=diagnose_,
                  format=format_, colorize=False,
                  rotation=rotation_, retention=retention_, encoding=encoding_, enqueue=True,
                  filter=lambda record: record["level"].no >= logger.level("DEBUG").no)
    # error 现在配置记录warn级别以上的
    my_logger.add(folder_ + prefix_ + "error.log", level="WARNING", backtrace=backtrace_, diagnose=diagnose_,
                  format=format_, colorize=False,
                  rotation=rotation_, retention=retention_, encoding=encoding_, enqueue=True,
                  filter=lambda record: record["level"].no >= logger.level("WARNING").no)
    my_logger.add(sys.stderr, level="CRITICAL", backtrace=backtrace_, diagnose=diagnose_,
                  format=format_, colorize=True,
                  filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)

    # 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
    # debug
    # logger.add(folder_ + prefix_ + "debug.log", level="DEBUG", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=False,
    #            rotation=rotation_, retention=retention_, encoding=encoding_,
    #            filter=lambda record: record["level"].no >= logger.level("DEBUG").no)
    #
    # # info
    # logger.add(folder_ + prefix_ + "info.log", level="INFO", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=False,
    #            rotation=rotation_, retention=retention_, encoding=encoding_,
    #            filter=lambda record: record["level"].no >= logger.level("INFO").no)
    #
    # # warning
    # logger.add(folder_ + prefix_ + "warning.log", level="WARNING", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=False,
    #            rotation=rotation_, retention=retention_, encoding=encoding_,
    #            filter=lambda record: record["level"].no >= logger.level("WARNING").no)
    #
    # # error
    # logger.add(folder_ + prefix_ + "error.log", level="ERROR", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=False,
    #            rotation=rotation_, retention=retention_, encoding=encoding_,
    #            filter=lambda record: record["level"].no >= logger.level("ERROR").no)
    #
    # # critical
    # logger.add(folder_ + prefix_ + "critical.log", level="CRITICAL", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=False,
    #            rotation=rotation_, retention=retention_, encoding=encoding_,
    #            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)
    #
    # logger.add(sys.stderr, level="CRITICAL", backtrace=backtrace_, diagnose=diagnose_,
    #            format=format_, colorize=True,
    #            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)

    # if not os.path.exists('config/logging_config.json'):
    #     sys.exit("no configs file")
    # with open('config/logging_config.json', 'r') as f:
    #     logging_config = json.load(f)
    #
    # logging.config.dictConfig(logging_config)


# def config_loguru():
#     file_name = "config/loguru_config.json"
#     if not os.path.exists(file_name):
#         sys.exit("no configs file")
#     with open(file_name, 'r') as f:
#         loguru_config = json.load(f)
#
#     logger.configure(**loguru_config)
#     logger.info("11111111111111111111111111111111111111111111111111111111111")

# def log_logging_with_loguru():
#     # logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
#     # handler = logging.handlers.SysLogHandler(address=('localhost', 514))
#     # logger.add(handler)
#     setup_loguru_logging_intercept(
#         level=logging.DEBUG,
#         modules=("root","telegram", "httpcore", "httpx")
#     )


# with open('config/logging_config.json', 'r') as f:
#     logging_config = json.load(f)
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

def init():
    # global this_log_queue
    # this_log_queue = log_queue
    config_logging(logger)
    # config_loguru()
    # log_logging_with_loguru()
    logger.info("inited logging")
    # global log_thread
    # log_thread = threading.Thread(target=logger_thread, args=(log_queue,))
    # log_thread.start()
