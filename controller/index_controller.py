import asyncio
import time

from flask import request, jsonify
from functools import wraps

from configure import config
from repository import v2ex_post_repo
from repository.v2ex_post_repo import V2exPost
from telebot.tgbot_funcs import send_message
from . import app
from service.v2ex_service import get_topics
from loguru import logger
import telebot.tgbot_funcs as tgbot


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


@app.after_request
def format_response(response):
    try:
        data = response.get_json()
        if data is None:
            data = response.get_data(as_text=True)
        timestamp = int(time.time())
        new_response_body = {
            "timestamp": timestamp,
            "data": data
        }
        response.set_data(jsonify(new_response_body).get_data())
        return response
    except Exception as e:
        print(e)
        return response


# def format_response(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         data, code = func(*args, **kwargs)
#
#         formatted_data = {
#             'timestamp': int(time.time()),
#             'data': data
#         }
#         return jsonify(formatted_data), code
#
#     return wrapper


# 处理 POST 请求的路由
@app.route('/send_message', methods=['POST'])
# @format_response
def send_message():
    # 从请求中获取 JSON 数据
    data = request.get_json()

    # # 校验字段
    # if not all(key in data for key in ('content', 'title', 'author')):
    #     return '缺少必要的字段', 400
    if 'content' not in data:
        return jsonify({'msg': '缺少必要的字段'}), 400
        # return '缺少必要的字段', 400
    content = data['content']
    if 'send_id' not in data:
        send_id = config.group_id
    else:
        send_id = data['send_id']
    # 发送消息到 Telegram 频道
    response = asyncio.run(tgbot.send_message(send_id, content))

    if response is not None:
        get_post = V2exPost(
            id=send_id,
            content=content,
            title='send_message',
            created=int(time.time()),
            replies=0,
            url='',
            last_modified=int(time.time()),
            telebot_chat_id=config.telebot_chat_id,
            telebot_message_id=response['message_id']
        )
        v2ex_post_repo.insert_posts(get_post)

    print(response)
    # 发送消息到 Telegram 频道
    # if bot and channel_id:
    #     bot.send_message(channel_id, f'内容：{content}\n 标题：{title}\n 作者：{author}')
    #     return '消息已发送', 200
    # else:
    #     return '未配置 Telegram Bot 或频道 ID', 500
    return '消息已发送', 200
