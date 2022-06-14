from config import BOT_TOKEN
import logging
import json
from typing import Dict
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Filters, ConversationHandler
from datetime import date
global users, ranktext,nametext
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
ENTERRANK, ENTERNAME, COMPLETE= range(3)
# Define a few command handlers. These usually take the two arguments update and
# context.


def setup(update: Update, context: CallbackContext) -> int:
    global userid
    user = update.effective_user
    userid=user.id

    update.message.reply_html(
        "<b>BOT SETUP</b>" "\n"
        "Please enter rank"
    )
    return ENTERRANK

def getrank(update: Update, context: CallbackContext) -> int:
    global ranktext, nametext
    ranktext=update.message.text
    print(ranktext)
    update.message.reply_text(fr"Please enter your name")
    return ENTERNAME
    
def getname(update: Update, context: CallbackContext) -> int:
    global ranktext, nametext
    nametext=update.message.text
    print(nametext)
    update.message.reply_text(fr"Your Rank and Name is {ranktext} {nametext}") 
    update.message.reply_text("Setup complete") 
    return COMPLETE
def done(update: Update, context: CallbackContext) -> None:
	update.message.reply_text("Setup complete")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    #add conv handler
    conv_handler = ConversationHandler(
   entry_points=[CommandHandler('setup', setup)],
        states={
            ENTERRANK: [
                MessageHandler(Filters.text & ~(Filters.command),getrank)
                ],
             ENTERNAME: [ MessageHandler(Filters.text & ~(Filters.command),getname)],
             COMPLETE: []
                },    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
                )
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
