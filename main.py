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
HQ=""
S1=""
S2=""
S3=""
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
ENTERRANK, ENTERNAME, ENTERSECTION, EDITPS = range(4)


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
       # print(users)
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
    keyboard = [
        [
            InlineKeyboardButton("HQ", callback_data='HQ'),
            InlineKeyboardButton("Section 1", callback_data='Section 1'),
        ],
        [InlineKeyboardButton("Section 2", callback_data='Section 2'),
         InlineKeyboardButton("Section 3", callback_data="Section 3"),
         ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    nametext = update.message.text
    print(nametext)
    users[userid]['Name'] = nametext
    #update.message.reply_text(fr"Your Rank and Name is {users[userid]['Rank']} {users[userid]['Name']}")
    #    update.message.reply_text(fr"{users}")
    update.message.reply_text("Please input your section", reply_markup=reply_markup)
    return ENTERSECTION


def getsection(update: Update, context: CallbackContext) -> None:
    global users, userid
    query=update.callback_query
    query.answer()
    sectiontext = query.data
    users[userid]['Section'] = str(sectiontext)
    users[userid]['PS']=""
    print(sectiontext)
    print(users)
    query.edit_message_text(fr"Section: {query.data}")
    query.message.reply_text(fr"Your Rank and Name is {users[userid]['Rank']} {users[userid]['Name']} and you're from {users[userid]['Section']}")
    userdata = json.dumps(users)
    with open('user_data.json', 'w') as outfile:
        outfile.write(userdata)
    query.message.reply_text("Setup Complete")
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


def paradestate(update: Update, context: CallbackContext) -> int:
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users
    with open('user_data.json') as json_file:
        users = json.load(json_file)
    #print(users)
    Totalstrength = 0
    Currentstrength = 0
    JurongCstrength = 0
    JurongTstrength = 0
    JurongLVE = 0
    JurongOFF = 0
    JurongMC = 0
    JurongOS = 0
    JurongAO = 0
    JurongOthers = 0
    JurongRSO = 0
    JurongRSI = 0
    JurongCourse = 0
    JurongMA = 0
    JLVE = ""
    JOFF = ""
    JMC = ""
    JMA = ""
    JRSO = ""
    JRSI = ""
    JOS = ""
    JAO = ""
    JCourse = ""
    JOTHERS = ""

    Totalstrength=JurongTstrength
    Currentstrength=JurongCstrength
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Off", callback_data='Off'),
            InlineKeyboardButton("Leave", callback_data='Leave'),
        ],
        [InlineKeyboardButton("MC", callback_data='MC'),
         InlineKeyboardButton("MA", callback_data="MA"),
         ],
        [
            InlineKeyboardButton("RSO", callback_data="RSO"),
            InlineKeyboardButton("RSI", callback_data="RSI")
        ],
        [
            InlineKeyboardButton("AO", callback_data="AO"),
            InlineKeyboardButton("OS", callback_data="OS")
        ],
        [
            InlineKeyboardButton("CSE", callback_data="Course"),
            InlineKeyboardButton("Others", callback_data="Others")
        ],
        [
            InlineKeyboardButton("Present", callback_data="Present")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for _ in users:
        JurongTstrength+=1
    if JurongLVE != 0:
        JLVE = fr'LVE:{JurongLVE}' + '\n'
    if JurongOFF != 0:
        JOFF = fr'OFF:{JurongOFF}' + '\n'
    if JurongMC != 0:
        JMC = fr'MC:{JurongMC}' + '\n'
    if JurongMA != 0:
        JMA = fr'MA:{JurongMA}' + '\n'
    if JurongOS != 0:
        JOS = fr'OS:{JurongOS}' + '\n'
    if JurongAO != 0:
        JAO = fr'AO:{JurongAO}' + '\n'
    if JurongRSO != 0:
        JRSO = fr'RSO:{JurongRSO}' + '\n'
    if JurongRSI != 0:
        JRSI = fr'RSI:{JurongRSI}' + '\n'
    if JurongCourse != 0:
        JCourse = fr'CSE:{JurongCourse}' + '\n'
    if JurongOthers != 0:
        JOTHERS = fr'Others:{JurongOthers}' + '\n'

    update.message.reply_html(
        fr'<b>31FMD Parade State - {today} </b>' '\n' '\n'
        fr'Total Strength: {Totalstrength}' '\n'
        fr'Current Strength: {Currentstrength}' '\n' '\n'
        '----------------------------------' '\n'
        fr'Jurong Total Strength: {JurongTstrength}' '\n'
        fr'Jurong Current Strength: {JurongCstrength}' '\n' '\n'
        fr'{JLVE}'
        fr'{JOFF}'
        fr'{JRSO}'
        fr'{JRSI}'
        fr'{JMA}'
        fr'{JMC}'
        fr'{JOS}'
        fr'{JAO}'
        fr'{JCourse}'
        fr'{JOTHERS}'
        '\n'
        '<b>HQ</b>' '\n'
        '\n' '<b>Section 1</b>' '\n'
        '\n' '<b>Section 2</b>' '\n'
        '\n' '<b>Section 3</b>', reply_markup=reply_markup

    )
    return EDITPS


def paradestateEdit(update: Update, context: CallbackContext, ) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users, userid, HQ, S1, S2, S3
    HQ = ""
    S1 = ""
    S2 = ""
    S3 = ""
    JurongLVE = 0
    JurongOFF = 0
    JurongMC = 0
    JurongOS = 0
    JurongAO = 0
    JurongOthers = 0
    JurongRSO = 0
    JurongRSI = 0
    JurongCourse = 0
    JurongMA = 0
    JurongCstrength = 0
    JLVE = ""
    JOFF = ""
    JMC = ""
    JMA = ""
    JRSO = ""
    JRSI = ""
    JOS = ""
    JAO = ""
    JCourse = ""
    JOTHERS = ""
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    user = update.effective_user
    userid = str(user.id)
  #  print(users[userid]["Rank"])
    #psname = fr"{psname}" + "\n" + fr"{users[userid]['Rank']} {users[userid]['Name']}"
    keyboard = [
        [
            InlineKeyboardButton("Off", callback_data='Off'),
            InlineKeyboardButton("Leave", callback_data='Leave'),
        ],
        [InlineKeyboardButton("MC", callback_data='MC'),
         InlineKeyboardButton("MA", callback_data="MA"),
         ],
        [
            InlineKeyboardButton("RSO", callback_data="RSO"),
            InlineKeyboardButton("RSI", callback_data="RSI")
        ],
        [
            InlineKeyboardButton("AO", callback_data="AO"),
            InlineKeyboardButton("OS", callback_data="OS")
        ],
        [
            InlineKeyboardButton("CSE", callback_data="Course"),
            InlineKeyboardButton("Others", callback_data="Others")
        ],
        [
            InlineKeyboardButton("Present", callback_data="Present")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    if query.data=='Off':
        users[userid]['PS'] = 'Off'
    if query.data=='Leave':
        users[userid]['PS'] = 'Leave'
    if query.data=='MC':
        users[userid]['PS'] = 'MC'
    if query.data=='MA':
        users[userid]['PS'] = 'MA'
    if query.data=='RSO':
        users[userid]['PS'] = 'RSO'
    if query.data=='RSI':
        users[userid]['PS'] = 'RSI'
    if query.data=='AO':
        users[userid]['PS'] = 'AO'
    if query.data=='OS':
        users[userid]['PS'] = 'OS'
    if query.data=='Course':
        users[userid]['PS'] = 'Course'
    if query.data=='Others':
        users[userid]['PS'] = 'Others'
    if query.data=='Present':
        users[userid]['PS'] = 'Present'
    userdata = json.dumps(users)
    with open('user_data.json', 'w') as outfile:
        outfile.write(userdata)
    for x in users:
        if users[x]["Section"] == 'HQ':
            HQ= HQ + fr'{users[x]["Rank"]} {users[x]["Name"]}: {users[x]["PS"]}' + '\n'
        if users[x]["Section"] == 'Section 1':
            S1= S1 + fr'{users[x]["Rank"]} {users[x]["Name"]}: {users[x]["PS"]}' + '\n'
        if users[x]["Section"] == 'Section 2':
            S2=S2 + fr'{users[x]["Rank"]} {users[x]["Name"]}: {users[x]["PS"]}' + '\n'
        if users[x]["Section"] == 'Section 3':
            S3=S3 + fr'{users[x]["Rank"]} {users[x]["Name"]}: {users[x]["PS"]}' + '\n'
        if users[x]["PS"] == "Off":
            JurongOFF+=1
        if users[x]["PS"] == "Leave":
            JurongLVE+=1
        if users[x]["PS"] == "MC":
            JurongMC+=1
        if users[x]["PS"] == "MA":
            JurongMA+=1
        if users[x]["PS"] == "RSO":
            JurongRSO+=1
        if users[x]["PS"] == "RSI":
            JurongRSI+=1
        if users[x]["PS"] == "AO":
            JurongAO+=1
        if users[x]["PS"] == "Course":
            JurongCourse+=1
        if users[x]["PS"] == "OS":
            JurongOS+=1
        if users[x]["PS"] == "Others":
            JurongOthers+=1
        if users[x]["PS"] == "Present":
            JurongCstrength+=1
    if JurongLVE != 0:
        JLVE = fr'LVE:{JurongLVE}' + '\n'
    if JurongOFF != 0:
        JOFF = fr'OFF:{JurongOFF}' + '\n'
    if JurongMC != 0:
        JMC = fr'MC:{JurongMC}' + '\n'
    if JurongMA != 0:
        JMA = fr'MA:{JurongMA}' + '\n'
    if JurongOS != 0:
        JOS = fr'OS:{JurongOS}' + '\n'
    if JurongAO != 0:
        JAO = fr'AO:{JurongAO}' + '\n'
    if JurongRSO != 0:
        JRSO = fr'RSO:{JurongRSO}' + '\n'
    if JurongRSI != 0:
        JRSI = fr'RSI:{JurongRSI}' + '\n'
    if JurongCourse != 0:
        JCourse = fr'CSE:{JurongCourse}' + '\n'
    if JurongOthers != 0:
        JOTHERS = fr'Others:{JurongOthers}' + '\n'
    Totalstrength=JurongTstrength
    Currentstrength=JurongCstrength
    query.edit_message_text(
        fr'<b>31FMD Parade State - {today} </b>' '\n' '\n'
        fr'Total Strength: {Totalstrength}' '\n'
        fr'Current Strength: {Currentstrength}' '\n' '\n'
        '----------------------------------' '\n'
        fr'Jurong Total Strength: {JurongTstrength}' '\n'
        fr'Jurong Current Strength: {JurongCstrength}' '\n' '\n'
        fr'{JLVE}'
        fr'{JOFF}'
        fr'{JRSO}'
        fr'{JRSI}'
        fr'{JMA}'
        fr'{JMC}'
        fr'{JOS}'
        fr'{JAO}'
        fr'{JCourse}'
        fr'{JOTHERS}'
        '\n'
        '<b>HQ</b>' '\n'
        fr'{HQ}'
        '\n' '<b>Section 1</b>' '\n' 
        fr'{S1}'
        '\n' '<b>Section 2</b>' '\n'
        fr'{S2}'
        '\n' '<b>Section 3</b>' '\n'
        fr'{S3}',  parse_mode='HTML', reply_markup=reply_markup

    )


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
            ENTERSECTION: [CallbackQueryHandler(getsection)],
        }, fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('ps', paradestate)],
        states={
            EDITPS: [CallbackQueryHandler(paradestateEdit)],
        }, fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler2)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
