from datetime import datetime as dt
import datetime as DT
import os
import pyodbc
import warnings
import calendar
import telegram
import re
import logging
import time

def handler():
    # BOT INITIALIZATION
    token = 'token_goes_here'
    bot = telegram.Bot(
        token=token
    )

    chat_id ='chat_id_goes_here'

    print(bot.get_me())
    print()
    updates = bot.get_updates()
    print([u.message.text for u in updates])


    from telegram.ext import Updater
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

  #Command handlers
    from telegram.ext import CommandHandler,MessageHandler,Filters
    info_help = CommandHandler('help', help)
    ping_handler = CommandHandler('ping', ping)
    reply_handler = CommandHandler('reply',responseExample)

  #Adds commands to dispacch handlers
    dispatcher.add_handler(info_help)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(reply_handler)
    

    updater.start_polling()

# FUCNTIONS BOT WILL RESPOND TO IF PROMTED

def ping(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I am Still Active :)")

def help(update, context):
    message = "<b>/ping</b> ~ bot will repond if system is active\n" \
            "<b>/help</b> ~ returns help list, duh\n" \
              "<b>/reply</b> <i>anything</i> ~ sends example user input reponse" 

    context.bot.send_message(chat_id=update.message.chat_id, text=message,parse_mode=telegram.ParseMode.HTML)

def responseExample(update, context):
    try:
        user_says = context.args[0].upper().strip()
        context.bot.send_message(chat_id=update.message.chat_id, text = "User response: " + user_says)
    except:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please specificy valid input...")


# I THINK YOU KNOW WHAT THIS IS

if __name__ == "__main__":

    #handler()

    try:
        # warnings.filterwarnings("ignore")
        print("Agent Initilialized! ~ you're welcome Matt")
        handler()
    except:
        print("Initialization failed! ~ shit Matt, what the fuck did you do?")


