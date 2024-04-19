from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import sessionmaker

from . import engine, TgUser,async_engine

Session = sessionmaker(bind=engine)

async_Session = sessionmaker(async_engine, class_=AsyncSession)

def insert_tg_user(tg_user: TgUser) -> TgUser:
    """
     增加记录
    :param tg_user:
    :return:
    """
    # 创建会话
    session = Session()
    session.add(tg_user)
    session.commit()
    session.close()
    return tg_user

async def new_tg_user(tg_user: TgUser):
    """
         增加记录
        :param tg_user:
        :return:
        """
    # 异步操作需要在'async with'块内执行
    async with async_Session() as session:
        # 异步方式开始事务
        async with session.begin():
            # 使用异步session操作数据库
            session.add(tg_user)

        # 异步提交
        await session.commit()




# session = Session()
# new_post = V2exPost(
#     url='http://example.com',
#     title='Example Post',
#     content='This is an example post.',
#     created=1234567890,
#     replies=0,
#     last_modified=1234567890
# )
# session.add(new_post)
# session.commit()

def get_tg_user(tg_user_id):
    """
    查询记录
    :param tg_user_id:
    :return:
    """
    session = Session()
    post = session.query(TgUser).filter_by(tg_id=tg_user_id).first()
    session.close()
    return post


def get_tg_user_by_uid(u_id):
    """
    查询记录
    :param tg_user_id:
    :return:
    """
    session = Session()
    post = session.query(TgUser).filter_by(id=u_id).first()
    session.close()
    return post


# # 查询记录
# tg_user = session.query(V2exPost).all()
# for post in tg_user:
#     print(post.title)

def update_tg_user(tg_user):
    """
    修改记录
    :param tg_user:
    :return:
    """
    session = Session()
    user = get_tg_user(tg_user.id)
    user.title = tg_user.title
    user.content = tg_user.content
    user.created = tg_user.created
    user.replies = tg_user.replies
    user.last_modified = tg_user.last_modified

    session.commit()
    session.close()


def delete_tg_user(tg_user_id):
    """
    删除记录
    :param tg_user_id:
    :return:
    """
    session = Session()
    post = session.query(TgUser).filter_by(id=tg_user_id).first()
    session.delete(post)
    session.commit()
    session.close()

# 关闭会话
# session.close()
