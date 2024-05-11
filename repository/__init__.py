import os.path
import sqlite3
from sqlalchemy import Column, Integer, String, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session

from entity import *
from entity.dbBase import init_db


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




# def check_db_async() -> AsyncEngine:
#     engine = create_async_engine(
#         'sqlite+aiosqlite:///' + db_path,
#         echo=True
#     )
#     # init_db(engine)
#     return engine


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
# async_engine = check_db_async()

# Session = sessionmaker(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
