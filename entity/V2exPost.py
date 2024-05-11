from sqlalchemy import create_engine, Column, Integer, String
from telegram.helpers import escape_markdown
from entity.dbBase import Base
from utils.datetime_helper import timestamp_int_2_str


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
