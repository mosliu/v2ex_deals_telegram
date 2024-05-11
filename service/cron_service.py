import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

from configure import config
from entity.V2exPost import V2exPost
from entity.TgUser import TgUser
from repository import v2ex_post_repo, crud, Session
from telebot.tgbot_funcs import send_message, edit_message_text
from . import logger, v2ex_service
import asyncio
import re
from configure import config
import ahocorasick


async def fetch_v2ex_job():
    if not config.start_cron_v2ex_job:
        return
    logger.info("start fetching v2ex job")
    got_json = v2ex_service.get_topics()
    results = got_json['result']
    for result in results:
        get_id = result.get('id', None)
        get_post = V2exPost(
            id=get_id,
            content=result.get('content', ''),
            title=result.get('title', ''),
            created=result.get('created', 0),
            replies=result.get('replies', 0),
            url=result.get('url', ''),
            last_modified=result.get('last_modified')
        )

        db_post = v2ex_post_repo.get_posts(get_id)
        if db_post:

            # v2ex_post_repo.update_posts(get_post)
            if (not db_post.last_modified == get_post.last_modified) or (not db_post.replies == get_post.replies):
                logger.info("modify post")
                # 修改了
                logger.info("v2ex post {} modified!", get_post.id)
                await edit_message_text(db_post.telebot_chat_id, db_post.telebot_message_id, get_post.get_post_text_(),
                                        parse_mode='MarkdownV2')
                v2ex_post_repo.update_posts(get_post)



        else:  # 如果不存在则 发送并 插入
            logger.info("got new post")
            # a = asyncio.run(send_message(config.group_id, f"新帖子: {get_post.title} {get_post.url}"))
            # a = await send_message(config.group_id, f"新帖子: {get_post.title} {get_post.url}", parse_mode='MarkdownV2')
            a = await send_message(config.channel_id, get_post.get_post_text_(), parse_mode='MarkdownV2')
            await check_and_send_watch(get_post)
            if a is not None:
                message_id = a['message_id']
                # get_post.telebot_chat_id = config.group_id
                get_post.telebot_chat_id = config.channel_id
                get_post.telebot_message_id = message_id
            else:
                get_post.telebot_chat_id = -1
                get_post.telebot_message_id = -1
            v2ex_post_repo.insert_posts(get_post)


# 为了防止主线程立即退出，我们在这里使用一个无限循环
# while True:
#     pass


user_word_dict = {}
inverted_index = {}
aca = ahocorasick.Automaton()


def invert_dict(user_word_dict):
    '''
    创建倒排索引
    :param user_word_dict:
    :return:
    '''

    inverted_dict = {}

    for user_id, word_list in user_word_dict.items():
        for word in word_list:
            # 获得包含当前单词的用户列表的引用
            # 不存在则返回默认值：空列表
            user_list = inverted_dict.get(word, [])

            # 把当前的用户ID添加到用户列表中
            user_list.append(user_id)

            # 更新倒排索引
            inverted_dict[word] = user_list

    return inverted_dict


async def check_and_send_watch(post: V2exPost) -> None:
    global user_word_dict
    global inverted_index
    if post is None:
        return

    hit_words = []
    # 开始查找
    # 该方法 匹配所有字符串
    for item in aca.iter(post.title):
        hit_words.append(item)
    for item in aca.iter(post.content):
        hit_words.append(item)
    send_user = []
    for word in hit_words:
        users = inverted_index.get(word[1])
        for userid in users:
            if userid not in send_user:
                # send
                await send_message(userid, post.get_post_text_())
                send_user.append(userid)


async def watch_words_job():
    global user_word_dict
    global inverted_index
    if not config.start_cron_watch_job:
        return
    db = Session()
    users = db.query(TgUser).filter(TgUser.watch_words != None).filter(TgUser.credit > 0).all()
    user_word_dict.clear()
    # user_word_dict = {user.tg_id: user.watch_words.split(",") for user in users}
    user_word_dict = {user.tg_id: re.split(",|，", user.watch_words) for user in users}
    # print(user_word_dict)
    inverted_index.clear()
    inverted_index = invert_dict(user_word_dict)
    # 将所有的单词串接在一起，形成一个大的列表
    all_words = [word for word in inverted_index.keys()]
    # 去重
    for word in all_words:
        aca.add_word(word, word)

    # 使用这些单词创建Trie树
    # for x in range(len(all_words)):
    #     aca.add_word(all_words[x], (x, all_words[x]))
    aca.make_automaton()


async def test_job():
    print("222222222222222222222222222222222222222222222")
    logger.info("testing job 222222222222222222")


def start_job():
    # fetch_v2ex_job()
    # 创建一个后台调度器
    # scheduler = BackgroundScheduler()
    # 添加一个每分钟运行一次的 cron 作业
    # scheduler.add_job(fetch_v2ex_job, 'cron', minute='*')
    # scheduler.add_job(fetch_v2ex_job, 'cron', second='*')
    scheduler = AsyncIOScheduler()
    job = scheduler.add_job(fetch_v2ex_job, 'interval', seconds=60,
                            next_run_time=datetime.now() + timedelta(seconds=10))
    job2 = scheduler.add_job(watch_words_job, 'interval', seconds=600, next_run_time=datetime.now())
    # job = scheduler.add_job(test_job, 'interval', seconds=5,next_run_time=datetime.now())
    scheduler.start()
    # asyncio.run(job.func())
    # 开始调度器
    logger.info("start scheduler")

    asyncio.get_event_loop().run_forever()
    # scheduler.start()
