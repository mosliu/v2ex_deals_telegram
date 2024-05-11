import time
from telegram import Update, Bot
from telegram.ext import ContextTypes, CallbackContext
from configure import config
from loguru import logger
import uuid
from sqlalchemy import inspect

from repository import tg_user_repo, Session, crud
from repository.tg_user_repo import TgUser

from utils.datetime_helper import timestamp_int_2_str

timestamp_format_str = "%Y-%m-%d %H:%M:%S"

db = Session()


async def create_user(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    user_id = update.effective_user.id
    exists_u = await get_user(user_id)
    if exists_u is not None:
        await update.message.reply_text(
            f'您的用户已经于{timestamp_int_2_str(exists_u.created_at)}创建，当前余额:{exists_u.credit}')
        return None

    # 新建一个TgUser对象
    user = TgUser(
        tg_id=user_id,
        # created_at=datetime.datetime.now()
        token=str(uuid.uuid4()),
        credit=100,
        created_at=time.time()

    )
    crud.add_entity(db, user)

    # tg_user_repo.insert_tg_user(user)
    # 不查询直接用的话，会报错，疑为异步问题
    # user =  await get_user(user_id)
    # user =tg_user_repo.get_tg_user(user_id)
    # time.sleep(1)
    context.user_data['tg_user'] = user
    await update.message.reply_text(f'您的用户已经成功创建，当前余额:{user.credit}')


async def user_watch(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = await get_user(update.effective_user.id)
    if exists_u is not None:
        await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”,可以使用 /modify_watch 命令修改')
        return None
    else:
        await update.message.reply_text(f'您尚未建立用户，使用/create 命令创建用户')


async def modify_watch(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = await get_user(update.effective_user.id)
    if exists_u is not None:
        await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”,请回复新的关注词，以逗号隔开')
        context.user_data['state'] = 'modify_watch'
        return None
    else:
        await update.message.reply_text(f'您尚未建立用户，使用 /create 命令创建用户')


async def modify_watch_word(update: Update, context: CallbackContext):
    logger.info("enter modify_watch_word")
    exists_u = await get_user(update.effective_user.id)
    ins(exists_u)
    if exists_u is not None:
        exists_u.watch_words = update.message.text
        tg_user_repo.insert_tg_user(exists_u)
        await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”')
        context.user_data['state'] = None


async def message_text_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data is None:
        return
    if context.user_data.get('state') == 'modify_watch':
        await modify_watch_word(update, context)
    else:
        pass


async def user_token(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = await get_user(update.effective_user.id)
    if exists_u is not None:
        await update.message.reply_text(f'您的用户 token:{exists_u.token}')
        return None
    else:
        await update.message.reply_text(f'您尚未建立用户，使用 /create 命令创建用户')

    # # 向发来 /start 的用户发送消息
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text=f"这是一个转存机器人")
    #


async def get_user(id):
    '''
    获取用户
    :param update:
    :return:
    '''
    # exists_u = crud.get_model_by_attribute(db, TgUser, model_id=id)
    exists_u = crud.get_model_by_attribute(db, TgUser, attribute="tg_id", attribute_value=id)
    # exists_u = tg_user_repo.get_tg_user(update.effective_user.id)
    return exists_u


# 显示对象库里面的状态
def ins(obj):
    ins = inspect(obj)
    print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending,
                                                                                ins.persistent, ins.detached))
