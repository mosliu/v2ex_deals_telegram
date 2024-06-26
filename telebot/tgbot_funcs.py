# tgbot_funcs.py

from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler
from configure import config
# from . import logger
from loguru import logger

bot = Bot(token=config.bot_token)


# 回复固定内容
async def start2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 定义一些行为

    # 向发来 /start 的用户发送消息
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"这是一个转存机器人")


async def error_callback(update: Update, context: CallbackContext):
    logger.error(f'Error happened:{context.error}')
    # print('Error happened:', context.error)


# 返回 ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update.effective_chat.id  可以就是与机器人交流的用户的 chat id
    your_chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'你的 chat id 是 {your_chat_id}')


async def message_other_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("enter message_other_handler")
    # 定义一些行为
    # 省略
    pass


async def send_message(chatid, text, parse_mode=None, reply_id=None):
    logger.info("calling send_message!!!!!")
    try:
        return await bot.send_message(
            chat_id=chatid,
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=reply_id,
        )
    except Exception as err:
        # logger.exception(f"{err.__class__.__name__}: {err} happend when sending message")
        logger.error(f"{err.__class__.__name__}: {err} happend when sending message,text:{text}")
    return None


async def edit_message_text(chatid, message_id, text, parse_mode=None):
    try:
        return await bot.edit_message_text(
            chat_id=chatid,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode
        )
    except Exception as err:
        logger.error(f"{err.__class__.__name__}: {err} happend when editing message")
    return None


async def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


async def button(update, context):
    query = update.callback_query

    query.answer()

    await query.edit_message_text(text="Selected option: {}".format(query.data))
