from configure import config, threads
from telegram import Update, Bot  # 获取消息队列的
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler

from log_config import InterceptHandler
from telebot.tg_user_funcs import create_user, user_watch, modify_watch, message_text_handler, user_token
from telebot.tgbot_funcs import start, message_other_handler, myid, error_callback, button
import logging
from multiprocessing import Process
from loguru import logger


# logger = logging.getLogger(__name__)


def init():
    logger.info('telebot start init')
    # p = Process(target=start_application, args=())
    # start_application()
    p = Process(target=start_application)
    p.deamon = True
    # 启动Flask应用
    p.start()
    threads.append(p)
    # queue_count_thread.start()
    # threads.append(queue_count_thread)
    # threading.Thread(target=start_application).start()
    logger.info('telebot init done')
    # logging.error('telebot init done')


def start_application():
    logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)
    # logger.info('111111111111111111111111111')
    # 创建实例的，在这里放入 token
    application = ApplicationBuilder().token(config.bot_token).build()

    # 类似路由，接收到 /start 执行哪个函数，左边是指令，右边是定义动作的函数
    # 注册 start_handler ，以便调度
    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('myid', myid))

    # application.add_error_handler(error_callback)

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # 当用户使用'/create' 命令时新建一个tguser对象
    # application.add_handler(MessageHandler(~filters.text & ~filters.private & ~filters.reply, create))
    application.add_handler(CommandHandler("create", create_user))
    # 当用户使用 '/watch' 命令时查看关注词
    application.add_handler(CommandHandler("watch", user_watch))
    application.add_handler(CommandHandler("modify_watch", modify_watch))
    application.add_handler(CommandHandler("token", user_token))

    # 分析指令之外的TEXT数据。
    application.add_handler(MessageHandler(filters.TEXT, message_text_handler))
    # (~filters.COMMAND)  就是指令之外的消息
    application.add_handler(MessageHandler((~(filters.COMMAND & filters.TEXT)), message_other_handler))

    # 启动，直到按 Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
