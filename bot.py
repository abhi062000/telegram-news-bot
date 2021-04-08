# POLLING

import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
# Enable logging
from telegram import Update, Bot
# logging: any kind of error happen or warning is raised, so this is used to parse it in a systematic manner
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# logger object can create logs for your program
logger = logging.getLogger(__name__)

TOKEN = "1789252593:AAE7L-RrEaxEITZvPGsY2TB75bZznc2m8Fk"

# https://python-telegram-bot.readthedocs.io/en/stable/ go to this link for referring the func usage

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "Ok"


def _help(update: Update, context: CallbackContext):
    help_txt = "Hey! This is help Text"
    update.message.reply_text(help_txt)

# error


def error(bot, update):
    # update.error contains error if caused due to update.
    logger.error("Update '%s' has caused error '%s", update, update.error)

# start


def greeting(update: Update, context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
    # print(update.to_dict().keys(),first_name)
    update.message.reply_text("hi {}".format(first_name))

# filter text gives echo


def message_handler(update: Update, context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)


def main():
    # updator will keep polling and receive the updates from telegram and move it to the dispatcher
    # updater = Updater(TOKEN)
    # dispatcher handles those updates
    # dp = updater.dispatcher  # all the response will be handled

    bot = Bot(TOKEN)
    bot.set_webhook("https://4e07be4bb442.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)

    # Add handlers
    # dispatcher needs multiple handlers
    # former start is for: if the user writes / with start then it will call the start(latter) function
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(CommandHandler("help", _help))
    # messageHandler class is for handling stickers and other text and if the msg is in text form user .text
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    # dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))  -> not working
    dp.add_error_handler(error)

    # updater.start_polling()
    # logger.info("Started polling...")
    # updater.idle()  # waits until the user presses ctrl+c or anything to stop the program


if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.set_webhook("https://4e07be4bb442.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    dp.add_error_handler(error)
    app.run(port=8443)


# code for older version of telegram-python-bot
# import logging
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# # enable logging
# logging.basicConfig(
#     format='%(asctime)s -%(name)s -%(levelname)s -%(message)s', level=logging.INFO)

# logger = logging.getLogger(__name__)

# TOKEN = "1789252593:AAE7L-RrEaxEITZvPGsY2TB75bZznc2m8Fk"


# def start(bot, update):
#     print(update)
#     author = update.message.from_user.first_name
#     reply = "Hi {}".format(author)
#     bot.send_message(chat_id=update.message.chat_id, text=reply)


# def _help(bot, update):
#     help_txt = "Hey! This is help Text"
#     bot.send_message(chat_id=update.message.chat_id, text=help_txt)


# def echo_text(bot, update):
#     reply = update.message.text
#     bot.send_message(chat_id=update.message.chat_id, text=reply)


# def echo_sticker(bot, update):
#     bot.send_sticker(chat_id=update.message.chat_id,
#                      sticker=update.message.sticker.file_id)


# def error(bot, update):
#     logger.error("Update '%s' caused error '%s' ", update, update.error)


# def main():
#     updater = Updater(TOKEN)  # check for any updates
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", _help))
#     dp.add_handler(MessageHandler(Filters.text, echo_text))
#     dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
#     dp.add_error_handler(error)

#     updater.start_polling()
#     logger.info("Started Polling...")
#     updater.idle()


# if __name__ == "__main__":
#     main()
