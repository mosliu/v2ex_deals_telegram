# tgbotBehavior.py
 
from telegram import Update  
from telegram.ext import ContextTypes  
 
import config  
 
# 回复固定内容  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    # 定义一些行为
 
    # 向发来 /start 的用户发送消息
    await context.bot.send_message(chat_id=update.effective_chat.id,  
                                   text=f"这是一个转存机器人")  
 
# 返回 ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    # update.effective_chat.id  可以就是与机器人交流的用户的 chat id
    your_chat_id = update.effective_chat.id  
 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'你的 chat id 是 {your_chat_id}')  
 
async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    # 定义一些行为
    # 省略
    pass