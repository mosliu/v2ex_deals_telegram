from sqlalchemy.orm import sessionmaker

from entity.V2exPost import V2exPost
from . import engine

Session = sessionmaker(bind=engine)


def insert_posts(v2_post):
    """
     增加记录
    :param v2_post:
    :return:
    """
    # 创建会话
    session = Session()
    session.add(v2_post)
    session.commit()
    session.close()


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

def get_posts(v2_post_id):
    """
    查询记录
    :param v2_post_id:
    :return:
    """
    session = Session()
    post = session.query(V2exPost).filter_by(id=v2_post_id).first()
    session.close()
    return post


# # 查询记录
# posts = session.query(V2exPost).all()
# for post in posts:
#     print(post.title)

def update_posts(v2_post):
    """
    修改记录
    :param v2_post:
    :return:
    """
    session = Session()
    post = get_posts(v2_post.id)
    post.title = v2_post.title
    post.content = v2_post.content
    post.created = v2_post.created
    post.replies = v2_post.replies
    post.last_modified = v2_post.last_modified

    session.commit()
    session.close()


# # 修改记录
# post = session.query(V2exPost).filter_by(title='Example Post').first()
# post.title = 'New Title'
# session.commit()
def delete_posts(v2_post_id):
    """
    删除记录
    :param v2_post_id:
    :return:
    """
    session = Session()
    post = session.query(V2exPost).filter_by(id=v2_post_id).first()
    session.delete(post)
    session.commit()
    session.close()

# # 删除记录
# post = session.query(V2exPost).filter_by(title='New Title').first()
# session.delete(post)
# session.commit()

# 关闭会话
# session.close()
