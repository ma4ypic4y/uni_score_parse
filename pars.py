import datetime
import math
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from score_parser import *
import asyncio

with open('.token', 'r') as file:
    TOKEN = file.read()

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hi {first_name}, nice to meet you!")

def text(update, context):
    s = str(stud_info(context) )
    saawd=0
    for i in range(1000000):
        saawd+=i
    update.message.reply_text( s +str(saawd))


dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(MessageHandler(Filters.text, text))

updater.start_polling()


updater.idle()