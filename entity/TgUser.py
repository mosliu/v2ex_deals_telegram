from sqlalchemy import  Column, Integer, String
# from entity import Base
from entity.dbBase import Base


# 创建基类
# Base =

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
