import time
from telegram import Update, Bot
from telegram.ext import ContextTypes, CallbackContext
from configure import config
from loguru import logger
import uuid

from repository import TgUser, tg_user_repo
from utils.datetime_helper import timestamp_int_2_str

timestamp_format_str = "%Y-%m-%d %H:%M:%S"


async def create_user(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = await get_user(update)
    if exists_u is not None:
        await update.message.reply_text(
            f'您的用户已经于{timestamp_int_2_str(exists_u.created_at)}创建，当前余额:{exists_u.credit}')
        return None

    # 新建一个TgUser对象
    user = TgUser(
        tg_id=update.effective_user.id,
        # created_at=datetime.datetime.now()
        token=str(uuid.uuid4()),
        credit=100,
        created_at=time.time()

    )

    tg_user_repo.insert_tg_user(user)
    # 不查询直接用的话，会报错，疑为异步问题
    user = tg_user_repo.get_tg_user(update.effective_user.id)
    # time.sleep(1)
    context.user_data['tg_user'] = user
    await update.message.reply_text(f'您的用户已经成功创建，当前余额:{user.credit}')


async def user_watch(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = await get_user(update)
    if exists_u is not None:
        await update.message.reply_text(
            f'您的用户已经于{timestamp_int_2_str(exists_u.created_at)}创建，当前余额:{exists_u.credit}')
        return None
    else:
        await update.message.reply_text(f'您尚未建立用户，使用/create 命令创建用户')


async def user_token(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = tg_user_repo.get_tg_user(update.effective_user.id)
    if exists_u is not None:
        await update.message.reply_text(
            f'您的用户 token:{exists_u.token}')
        return None
    else:
        await update.message.reply_text(f'您尚未建立用户，使用/create 命令创建用户')

    # # 向发来 /start 的用户发送消息
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text=f"这是一个转存机器人")
    #


async def get_user(update):
    '''
    获取用户
    :param update:
    :return:
    '''
    exists_u = tg_user_repo.get_tg_user(update.effective_user.id)
    return exists_u
