import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from telegram import Update, Bot, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1789252593:AAE7L-RrEaxEITZvPGsY2TB75bZznc2m8Fk"


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


def error(bot, update):
    logger.error("Update '%s' has caused error '%s", update, update.error)


def greeting(update: Update, context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
    update.message.reply_text("Hi {}".format(first_name))


def news(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.to_dict()[
        'message']['chat']['id'], text="Choose a category", reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def message_handler(update: Update, context: CallbackContext):
    intent, reply = get_reply(update.to_dict()['message']['text'], update.to_dict()[
        'message']['chat']['id'])

    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            update.message.reply_text(article['link'])
    else:
        update.message.reply_text(reply)

 bot = Bot(TOKEN)
bot.set_webhook("https://a0c80c361a97.ngrok.io/" + TOKEN)
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", greeting))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, message_handler))
dp.add_error_handler(error)
 
if __name__ == "__main__":   
    app.run(port=8443)
