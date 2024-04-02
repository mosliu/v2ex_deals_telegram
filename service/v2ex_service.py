import json

import requests

from configure import config


def get_topics(topic_name='all4all'):
    """
    获取 v2ex 某个节点下的所有帖子
    :param topic_name:
    :return:
    """
    token = config.v2ex_token
    url = f'https://www.v2ex.com/api/v2/nodes/{topic_name}/topics'
    headers = {
        'Authorization': f'Bearer {token}',  # 将 YOUR_TOKEN 替换为你的 token
    }
    response = requests.get(url, headers=headers)
    print('res.headers', response.headers)
    content = response.content
    print('res.content', content)
    loads = json.loads(content)
    response.close()
    return loads
