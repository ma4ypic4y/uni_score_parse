import datetime
import math
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


with open('.token', 'r') as file:
    TOKEN = file.read()

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hi {first_name}, nice to meet you!")

dispatcher.add_handler(CommandHandler("start", start))


updater.start_polling()

updater.idle()