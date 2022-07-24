import datetime
import math

from requests import ReadTimeout
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from score_parser import *

with open('.token', 'r') as file:
    TOKEN = file.read()

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hi {first_name}, nice to meet you!")

def create_message(name):
    data,date = stud_info(name)
    
    message = '*Дата последнего обновления*\n'
    message+= f'🗓{date[0]}   ⏰{date[1]} \n'
    message+=f'\n'
    for d in data:
        message+=f'📖{d["program"]}:\n'
        message+=f'Форма обучения 💸: {d["form_education"]}\n'
        message+=f'Сумма баллов 👉: {d["score"]}\n'
        message+=f'Документ 📕: {d["doc_type"]}\n'
        message+=f'Место в рейтинге 🎖: {d["stud_pos"]}/{d["num_all"]}  \n'
        print(d["stud_orig_pos"])
        if d["stud_orig_pos"][0]!='-':
            message+=f'Место среди оригиналов 🏆: {d["stud_orig_pos"]}/{d["num_orig"]} \n'
        else:
            message+=f'Если подать оригинал ⁉: {d["stud_orig_pos"][1:]}/{d["num_orig"]} \n'
        message+=f'Всего мест🦣: {d["places"]}\n'
        message+=f'\n'
    return message

def echo(update, context):
    return  update.message.reply_text(create_message(update.message.text))




dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()



updater.idle()