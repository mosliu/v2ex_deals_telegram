import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

from configure import config
from repository import *
from telebot.tgbot_funcs import send_message, edit_message_text
from . import logger, v2ex_service
import asyncio


async def fetch_v2ex_job():
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
            a = await send_message(config.group_id, get_post.get_post_text_(), parse_mode='MarkdownV2')
            if a is not None:
                message_id = a['message_id']
                get_post.telebot_chat_id = config.group_id
                get_post.telebot_message_id = message_id
            else:
                get_post.telebot_chat_id = -1
                get_post.telebot_message_id = -1
            v2ex_post_repo.insert_posts(get_post)


# 为了防止主线程立即退出，我们在这里使用一个无限循环
# while True:
#     pass

def start_job():
    # fetch_v2ex_job()
    # 创建一个后台调度器
    # scheduler = BackgroundScheduler()
    # 添加一个每分钟运行一次的 cron 作业
    # scheduler.add_job(fetch_v2ex_job, 'cron', minute='*')
    # scheduler.add_job(fetch_v2ex_job, 'cron', second='*')
    scheduler = AsyncIOScheduler()
    job = scheduler.add_job(fetch_v2ex_job, 'interval', seconds=60)
    scheduler.start()
    asyncio.run(job.func())
    # 开始调度器
    logger.info("start scheduler")
    # scheduler.start()
