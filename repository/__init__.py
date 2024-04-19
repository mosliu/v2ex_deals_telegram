import os.path
import sqlite3
from sqlalchemy import Column, Integer, String, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from sqlalchemy import create_engine
from telegram.helpers import escape_markdown

from utils.datetime_helper import timestamp_int_2_str

# from . import V2exPost

# 创建基类
Base = declarative_base()


# 定义v2ex_post表对应的类
class V2exPost(Base):
    __tablename__ = 'v2ex_post'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    content = Column(String)
    created = Column(Integer)
    replies = Column(Integer)
    last_modified = Column(Integer)
    telebot_chat_id = Column(Integer)
    telebot_message_id = Column(Integer)

    def get_post_text_(self) -> str:
        title_md = escape_markdown(self.title, 2)
        content_md = escape_markdown(self.content, 2)
        create_time = escape_markdown(timestamp_int_2_str(self.created), 2)
        last_modified_time = escape_markdown(timestamp_int_2_str(self.last_modified), 2)
        return f"[*{title_md}*]({self.url})\n\n{content_md}\n发布时间：{create_time}\n最后修改：{last_modified_time}\n回复数：{self.replies}"


class TgUser(Base):
    __tablename__ = 'tg_user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    token = Column(String)
    watch_words = Column(String)
    credit = Column(Integer)
    created_at = Column(Integer)
    last_modified = Column(Integer)
    telebot_chat_id = Column(Integer)
    telebot_message_id = Column(Integer)


def init_db(engine):
    # 创建表
    Base.metadata.create_all(engine)


def check_db() -> Engine:
    #
    # # 连接数据库（如果数据库文件不存在，会自动创建）
    # conn = sqlite3.connect(db_path)
    #
    # # 创建一个游标对象
    # c = conn.cursor()
    #
    # # 判断表是否存在，不存在就创建一个
    # c.execute("""
    #     create table v2ex_post
    #     (
    #         id            integer not null  primary key,
    #         url           TEXT,
    #         title         TEXT,
    #         content       TEXT,
    #         created       integer,
    #         replies       integer,
    #         last_modified integer
    #     );
    # """)
    #
    # # 提交事务
    # conn.commit()
    #
    # # 关闭连接
    # conn.close()

    # 创建数据库引擎
    engine = create_engine(
        'sqlite:///' + db_path,
        echo=True,
        pool_size=int(20),  # 连接池大小
        max_overflow=int(80),  # 连接池最大的大小
        # pool_recycle=int(config.SQLALCHEMY_POOL_RECYCLE),  # 多久时间主动回收连接，见下注释
    )
    init_db(engine)
    return engine


def check_db_async() -> AsyncEngine:
    engine = create_async_engine(
        'sqlite+aiosqlite:///' + db_path,
        echo=True
    )
    # init_db(engine)
    return engine


def check_db_dir():
    # 如果数据库文件所在的目录不存在，创建它
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


# 数据库文件路径
db_dir = './db/'
db_file = 'v2ex.db'
db_path = os.path.join(db_dir, db_file)
check_db_dir()
engine = check_db()
async_engine = check_db_async()

__all__ = ['v2ex_post_repo', 'V2exPost']
