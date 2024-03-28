from telegram import Update  # 获取消息队列的
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import preprocess
import config
# 从 tgbotBehavior.py 导入定义机器人动作的函数
from tgbotBehavior import start, transfer, myid

if __name__ == '__main__':
    # 创建实例的，在这里放入 token
    application = ApplicationBuilder().token(config.bot_token).build()

    # 类似路由，接收到 /start 执行哪个函数，左边是指令，右边是定义动作的函数
    start_handler = CommandHandler('start', start)
    # (~filters.COMMAND)  就是指令之外的消息
    transfer_handler = MessageHandler((~filters.COMMAND), transfer)
    #
    myid_handler = CommandHandler('myid', myid)

    # 注册 start_handler ，以便调度
    application.add_handler(start_handler)
    application.add_handler(transfer_handler)
    application.add_handler(myid_handler)

    # 启动，直到按 Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)