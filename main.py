from config import BOT_TOKEN
import logging
import json
from typing import Dict
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Filters, ConversationHandler
from datetime import date
global users
today = date.today()
today = str(today)
today = today.split("-")
dateorder = [2, 1, 0]
today = [today[i] for i in dateorder]
today = ''.join(today)
print(today)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
userid=1234
users = {
userid: {'Rank': "", 'Name': "", 'ParadeState': ""}
        }
RankIn, NameIn, ParadeStateIn = range(3)
# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_id = user.id
    update.message.reply_html(
        fr'Hi {user.mention_html()}\!{chat_id}', )


def setup(update: Update, context: CallbackContext) -> None:
    global userid
    user = update.effective_user
    userid=user.id

    update.message.reply_html(
        "<b>BOT SETUP</b>"
    )

def getrank(update: Update, context: CallbackContext) -> None:
    update.message.reply_html( "Please input rank")
    text=update.message.text
    print(text)


def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        'Help not available yet, good luck', )

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("setup", setup))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
