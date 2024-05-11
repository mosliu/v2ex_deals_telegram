import time
from telegram import Update, Bot
from telegram.ext import ContextTypes, CallbackContext
from configure import config
from loguru import logger
import uuid
from sqlalchemy import inspect
from functools import wraps
from repository import tg_user_repo, Session, crud
from repository.tg_user_repo import TgUser

from utils.datetime_helper import timestamp_int_2_str

timestamp_format_str = "%Y-%m-%d %H:%M:%S"

db = Session()


def checkuser(f):
    '''
    首先执行了用户存在性检查，如果用户不存在，我就发送一条提示信息并返回。如果用户存在，我就调用原来的函数 f。你可以使用这个装饰器来修饰任何需要进行用户存在性检查的函数。
    :param f:
    :return:
    '''

    @wraps(f)
    async def decorated(update: Update, context: CallbackContext) -> None:
        # 检查是否已经创建了TgUser对象
        # exists_u = await get_user(update.effective_user.id)
        exists_u = crud.get_model_by_attribute(db, TgUser, attribute="tg_id", attribute_value=update.effective_user.id)
        if exists_u is None:
            await update.message.reply_text(f'您尚未建立用户，使用 /create 命令创建用户')
            return None
        context.user_data['tg_user'] = exists_u
        return await f(update, context)

    return decorated


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


@checkuser
async def user_watch(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    # exists_u = await get_user(update.effective_user.id)
    exists_u = context.user_data['tg_user']
    if exists_u.watch_words is not None:
        await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”,可以使用 /modify_watch 命令修改')
    else:
        await update.message.reply_text(f'您当前无关注词,可以使用 /modify_watch 命令修改')
    return None


@checkuser
async def modify_watch(update: Update, context: CallbackContext) -> None:
    exists_u = context.user_data['tg_user']
    # 检查是否已经创建了TgUser对象
    await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”,请回复新的关注词，以逗号隔开.输入null或者None则关闭watch功能')
    context.user_data['state'] = 'modify_watch'
    return None


@checkuser
async def modify_watch_word(update: Update, context: CallbackContext) -> None:
    # logger.info("enter modify_watch_word")
    exists_u = context.user_data['tg_user']

    # 输入null或者None则关闭watch功能
    if update.message.text is None:
        return
    elif (update.message.text.lower() == 'null') or(update.message.text.lower() == 'none'):
            exists_u.watch_words = None
            await update.message.reply_text(f'您的关注词已取消')
    else:
        exists_u.watch_words = update.message.text
        await update.message.reply_text(f'您的关注词当前为“{exists_u.watch_words}”')
    crud.add_entity(db, exists_u)
    # tg_user_repo.insert_tg_user(exists_u)
    context.user_data['state'] = None


async def message_text_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data is None:
        return
    if context.user_data.get('state') == 'modify_watch':
        await modify_watch_word(update, context)
    else:
        pass


@checkuser
async def user_token(update: Update, context: CallbackContext) -> None:
    # 检查是否已经创建了TgUser对象
    exists_u = context.user_data['tg_user']
    # exists_u = await get_user(update.effective_user.id)
    await update.message.reply_text(f'您的用户 token:{exists_u.token}')
    return None

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
