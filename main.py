from config import BOT_TOKEN
import os
from os.path import exists
import logging
import json
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, \
    Filters, ConversationHandler
from datetime import date

global users, ranktext, nametext

users = {}
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
ENTERRANK, ENTERNAME = range(2)


# Define a few command handlers. These usually take the two arguments update and
# context.


def setup(update: Update, context: CallbackContext) -> int:
    # Create new file if no file found
    if not os.path.exists("user_data.json"):
        with open('user_data.json', 'w') as f:
            f.write("{}")
            print("New file created")
    global userid, users, userexist
    user = update.effective_user
    userid = str(user.id)
    # Read file and check for user
    with open('user_data.json') as json_file:
        users = json.load(json_file)
        print(users)
    if userid in users:
        update.message.reply_html("User already exists")
        userexist = True
    else:
        userexist = False
    update.message.reply_html(
        "<b>BOT SETUP</b>" "\n"
        "Please enter rank"
    )
    return ENTERRANK


def getrank(update: Update, context: CallbackContext) -> int:
    global ranktext, nametext, users, userid, userexist
    ranktext = update.message.text
    print(ranktext)
    if users == {}:
        users = {userid: {"Rank": ranktext}}  # If file empty
    elif userexist:
        users[userid]["Rank"] = ranktext  # If old user
    else:
        users[userid] = {}
        users[userid]["Rank"] = ranktext  # If new user
    update.message.reply_text(fr"Please enter your name")
    return ENTERNAME


def getname(update: Update, context: CallbackContext) -> int:
    global nametext, users, userid
    nametext = update.message.text
    print(nametext)
    users[userid]['Name'] = nametext
    update.message.reply_text(fr"Your Rank and Name is {users[userid]['Rank']} {users[userid]['Name']}")
    #    update.message.reply_text(fr"{users}")
    userdata = json.dumps(users)
    with open('user_data.json', 'w') as outfile:
        outfile.write(userdata)
    update.message.reply_text("Setup complete")
    return ConversationHandler.END


def done(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Setup complete")


def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    update.message.reply_html(
        '/help to display this text' '\n'
        '/setup to setup the bot with your info' '\n', )


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_id = user.id
    update.message.reply_html(
        fr'Hi {user.mention_html()}\!{chat_id}', )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # add conv handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setup', setup)],
        states={
            ENTERRANK: [
                MessageHandler(Filters.text & ~(Filters.command), getrank)
            ],
            ENTERNAME: [MessageHandler(Filters.text & ~(Filters.command), getname)],
        }, fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
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
