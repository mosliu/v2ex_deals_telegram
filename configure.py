import argparse
import os
import sys
import ruamel.yaml

from multiprocessing import Queue


class Config(object):
    def __init__(self, configs_path='./configs.yaml') -> None:
        self.yaml = ruamel.yaml.YAML()
        self.configs_path = os.path.abspath(configs_path)
        self.reload()
        #
        # self.author_webnote = "https://forward.vfly2.eu.org/"
        # # 指定 JSON 文件路径
        # self.json_file = 'path_dict.json'
        # self.store_dir = './forward_message/'  # 存储 转存（forward）消息 的目录
        # self.backupdir = './backup/'  # 绝对路径自然搜索以 / 开头，相对路径要以 ./ 开头 ,以 '/' 结尾
        #
        # # 加载数据
        # # 如果文件存在，则加载数据到字典；否则创建一个新的空字典
        # if os.path.exists(self.json_file):
        #     with open(self.json_file, 'r') as file:
        #         self.path_dict = json.load(file)
        # else:
        #     self.path_dict = {}
        #
        # # 图片列表和其说明文字   {'userid':['image1_url','image2_url'], 'userid_text':'text', etc} 结构是这样的，图片列表，说明字符串
        # self.image_list = {}
        # # 与图片有关的选项，如排列方式，gif 的时间间隔等。 key 是用户 id + 描述字符，值是对应的内容。
        # self.image_option = {}
        # # 如排列方式，key 为 id_array，值是一个元组
        # # 时间间隔，key 为 id_time，值是数字 秒
        #
        # self.urls_cache_dict = OrderedDict()
        # self.images_cache_dict = OrderedDict()

    def _load_config(self) -> dict:
        if not os.path.exists(self.configs_path):
            sys.exit("no configs file")
        else:
            shadow_path = None
            if self.configs_path.endswith('.yaml'):
                shadow_path = self.configs_path[:-5] + '_shadow.yaml'
            if self.configs_path.endswith('.yml'):
                shadow_path = self.configs_path[:-4] + '_shadow.yml'
            if (shadow_path is not None) and (os.path.exists(shadow_path)):
                with open(shadow_path, "r", encoding='utf-8') as fp:
                    configs = self.yaml.load(fp)
            else:
                with open(self.configs_path, "r", encoding='utf-8') as fp:
                    configs = self.yaml.load(fp)
            return configs

    def _proxy_set(self) -> None:
        if self.proxy is not None:
            os.environ["http_proxy"] = self.proxy
            os.environ["https_proxy"] = self.proxy
        # system = platform.system()  # 获取操作系统名字
        # if system == 'Windows':
        #     # 处于开发环境
        #     os.environ["http_proxy"] = "http://127.0.0.1:7890"
        #     os.environ["https_proxy"] = "http://127.0.0.1:7890"
        # elif system == 'Linux':
        #     # 处于生产环境
        #     pass
        # else:
        #     # 直接退出
        #     sys.exit('Unknown system.')

    def reload(self) -> None:
        configs = self._load_config()
        self.is_production = configs.get('is_production', False)
        self.chat_id = configs.get('chat_id', '')
        self.bot_token = configs.get('bot_token', '')
        self.proxy = configs.get('proxy', None)
        self.listen_ip = configs.get('listen_ip', '0.0.0.0')
        self.listen_port = configs.get('listen_port', 8744)
        self.v2ex_token = configs.get('v2ex_token', None)
        self.channel_id = configs.get('channel_id', '')
        self.group_id = configs.get('group_id', '')
        self.start_tele_bot = configs.get('start_tele_bot', False)
        self.start_cron_job = configs.get('start_cron_job', False)
        self._proxy_set()
        # self.push_dir = configs.get('push_dir')   # 转发目录
        # self.domain = configs.get('domain')   # 查看转存内容的网址的域名
        # self.netstr = configs.get('path')
        # self.command2exec = configs.get('exec')   # 在发送 \push 指令后，执行一个命令，设计用于自定义推送，比如 curl 到 webnote
        # self.manage_id = [self.chat_id, 1111111111]  # 管理员 id，放的是数字
        #
        # self.bot_username = configs.get('bot_username', '')
        # # 有特殊规则的频道
        # self.special_channel = configs.get('special_channel', {})
        # self.only_url_channel = self.special_channel.get('only_url', {})  # 应用特殊提取规则的频道
        # self.image_channel = self.special_channel.get('image', {})  # 对里面的频道应用特殊提取规则，也就是会考虑图片
        #
        # # 对文件处理的一些参数
        # self.process_file = configs.get('process_file', {})
        # self.gif_max_width = self.process_file.get('gif_max_width', 300)   # gif 最大的宽默认取 300 像素
        # self.video_max_size = self.process_file.get('video_max_size', 25)   # 接收视频的体积不能超过，默认取 25 MB，防止被刷，发个几百兆的转 GIF


def parse_parameters():
    global configfile
    # 创建一个解析器
    parser = argparse.ArgumentParser(description="Your script description")
    # 添加你想要接收的命令行参数
    parser.add_argument('--config', required=False, default='./config.yaml', help='Config File Path', )
    # 解析命令行参数
    args = parser.parse_args()
    # 将参数值赋给你的变量
    configfile = args.config
    return configfile


# 定义所有变量
config = Config(parse_parameters())

threads = []
