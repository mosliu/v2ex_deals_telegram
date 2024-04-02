import asyncio

from configure import config
from telebot.tgbot_funcs import send_message
from . import app
from repository import *
from service.v2ex_service import get_topics
from loguru import logger


@app.route('/')
def index():
    logger.info('index')
    return '.'


@app.route('/1')
def index2():
    # got_json = get_topics('all4all')
    # results = got_json['result']
    # for result in results:
    #     post = V2exPost(
    #         id=result.get('id', None),
    #         content=result.get('content', ''),
    #         title=result.get('title', ''),
    #         created=result.get('created', 0),
    #         replies=result.get('replies', 0),
    #         url=result.get('url', ''),
    #         last_modified=result.get('last_modified')
    #     )
    #     v2ex_post_repo.insert_posts(post)
    # asyncio.run(send_message(config.group_id, '*bold \*text*; _italic \*text_; __underline__', parse_mode='MarkdownV2'))

    return 'aa'
