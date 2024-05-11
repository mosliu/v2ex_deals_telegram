from sqlalchemy.ext.declarative import declarative_base

# 创建基类
Base = declarative_base()
def init_db(engine):
    # 创建表
    Base.metadata.create_all(engine)
