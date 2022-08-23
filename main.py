from config import BOT_TOKEN
import os
import telegramcalendar
from os.path import exists
import logging
import json
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, \
    Filters, ConversationHandler
from datetime import date

# bot = Bot(BOT_TOKEN)
global users, ranktext, nametext
HQ = ""
S1 = ""
S2 = ""
S3 = ""
am = 0
pm = 0
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
ENTERRANK, ENTERNAME, ENTERSECTION, EDITPS, END, ENTERSTUFF, EDITMESSAGE, ENTERDATE = range(8)


# Define a few command handlers. These usually take the two arguments update and
# context.


def setup(update: Update, context: CallbackContext) -> int:
    # Create new file if no file found
    if not os.path.exists("user_data.json"):
        with open('user_data.json', 'w') as f:
            f.write("{}")
            print("New file created")
    global users, userexist
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
    global ranktext, nametext, users, userexist
    ranktext = update.message.text
    user = update.effective_user
    userid = str(user.id)
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
    global nametext, users
    user = update.effective_user
    userid = str(user.id)
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
    # update.message.reply_text(fr"Your Rank and Name is {users[userid]['Rank']} {users[userid]['Name']}")
    #    update.message.reply_text(fr"{users}")
    update.message.reply_text("Please input your section", reply_markup=reply_markup)
    return ENTERSECTION


def getsection(update: Update, context: CallbackContext) -> None:
    global users
    user = update.effective_user
    userid = str(user.id)
    query = update.callback_query
    query.answer()
    sectiontext = query.data
    users[userid]['Section'] = str(sectiontext)
    users[userid]['AMPS'] = ""
    users[userid]['PMPS'] = ""
    users[userid]['amtext'] = ""
    users[userid]['pmtext'] = ""
    users[userid]['enddate'] = ""
    print(sectiontext)
    print(users)
    query.edit_message_text(fr"Section: {query.data}")
    query.message.reply_text(
        fr"Your Rank and Name is {users[userid]['Rank']} {users[userid]['Name']} and you're from {users[userid]['Section']}")
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
    chat_id = str(user.id)
    update.message.reply_html(
        fr'Hi {user.mention_html()}\!{chat_id}', )


def end(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(
        "Parade State Ended", )
    return ConversationHandler.END


def getstuff(update: Update, context: CallbackContext) -> None:
    print("GETSTUFFBOII")
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users, HQ, S1, S2, S3, am, pm, query
    user = update.effective_user
    chatid = str(user.id)
    text = update.message.text

    if am == 1:
        users[chatid]["amtext"] = text
    elif pm == 1:
        users[chatid]["pmtext"] = text
    else:
        users[chatid]["amtext"] = text
        users[chatid]["pmtext"] = text
    pm = 0
    if query.data == "OS" or am == 1:
        am = 0
        paradestateEditMessage(Update, CallbackContext)
        return EDITPS
    else:
        update.message.reply_html("Please select end date", reply_markup=telegramcalendar.create_calendar())
        return ENTERDATE


def getDate(update: Update, context: CallbackContext) -> None:
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users, HQ, S1, S2, S3, am, pm
    user = update.effective_user
    userid = str(user.id)
    query2 = update.callback_query
    query2.answer()
    bot = context.bot
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        query2.edit_message_text(fr"You selected {date.date()}")
        am = 0
        pm = 0
        EndDate = str(date.date())
        EndDate = EndDate.split("-")
        EndDate.pop(0)
        if EndDate[0] == '01':
            EndDate[0] = "Jan"
        elif EndDate[0] == '02':
            EndDate[0] = "Feb"
        elif EndDate[0] == '03':
            EndDate[0] = "Mar"
        elif EndDate[0] == '04':
            EndDate[0] = "Apr"
        elif EndDate[0] == '05':
            EndDate[0] = "May"
        elif EndDate[0] == '06':
            EndDate[0] = "Jun"
        elif EndDate[0] == '07':
            EndDate[0] = "Jul"
        elif EndDate[0] == '08':
            EndDate[0] = "Aug"
        elif EndDate[0] == '09':
            EndDate[0] = "Sep"
        elif EndDate[0] == '10':
            EndDate[0] = "Oct"
        elif EndDate[0] == '11':
            EndDate[0] = "Nov"
        elif EndDate[0] == '12':
            EndDate[0] = "Dec"
        print(EndDate)
        EndDate.reverse()
        EndDate = "-".join(EndDate)
        print(EndDate)
        users[userid]["enddate"] = EndDate
        print(date.date())
        userdata = json.dumps(users)
        with open('user_data.json', 'w') as outfile:
            outfile.write(userdata)
        paradestateEditMessage(Update, CallbackContext)
        return EDITPS


def paradestate(update: Update, context: CallbackContext) -> int:
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users
    with open('user_data.json') as json_file:
        users = json.load(json_file)
    # print(users)
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
    for _ in users:
        users[_]['AM'] = 0
        users[_]['PM'] = 0
    print(users)
    Totalstrength = JurongTstrength
    Currentstrength = JurongCstrength
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("AM", callback_data='AM'),
            InlineKeyboardButton("PM", callback_data='PM'),
        ],
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
        JurongTstrength += 1
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
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users, HQ, S1, S2, S3, am, pm, query

    query = update.callback_query
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
    print(userid)

    #  print(users[userid]["Rank"])
    # psname = fr"{psname}" + "\n" + fr"{users[userid]['Rank']} {users[userid]['Name']}"

    query.answer()
    if userid not in users:
        query.message.reply_html(fr'{user.mention_html()} Please initate the bot')
        query.message.reply_html("http://telegram.me/Parade_State_31_Bot?start=start")
    if query.data == "AM":
        am = 1
        users[userid]['AM'] = am
        print(am)
    if query.data == "PM":
        pm = 1
        users[userid]['PM'] = pm
        print(pm)

    if am == 1 and pm == 0:
        if query.data == 'Off':
            users[userid]['AMPS'] = 'Off'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'Leave':
            users[userid]['AMPS'] = 'Leave'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'MC':
            users[userid]['AMPS'] = 'MC'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'MA':
            users[userid]['AMPS'] = 'MA'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSO':
            users[userid]['AMPS'] = 'RSO'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSI':
            users[userid]['AMPS'] = 'RSI'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'AO':
            users[userid]['AMPS'] = 'AO'
            users[userid]['amtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'OS':
            users[userid]['AMPS'] = 'OS'
            users[userid]['amtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Course':
            users[userid]['AMPS'] = 'Course'
            users[userid]['amtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Course name?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Others':
            users[userid]['AMPS'] = 'Others'
            users[userid]['amtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Please enter your parade state.",
                                          parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Present':
            users[userid]['AMPS'] = 'Present'
            users[userid]['amtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
    elif am == 0 and pm == 1:
        if query.data == 'Off':
            users[userid]['PMPS'] = 'Off'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'Leave':
            users[userid]['PMPS'] = 'Leave'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'MC':
            users[userid]['PMPS'] = 'MC'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'MA':
            users[userid]['PMPS'] = 'MA'
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSO':
            users[userid]['PMPS'] = 'RSO'
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSI':
            users[userid]['PMPS'] = 'RSI'
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'AO':
            users[userid]['PMPS'] = 'AO'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'OS':
            users[userid]['PMPS'] = 'OS'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Course':
            users[userid]['PMPS'] = 'Course'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Course Name?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Others':
            users[userid]['PMPS'] = 'Others'
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Please enter your parade state.",
                                          parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Present':
            users[userid]['PMPS'] = 'Present'
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
    elif am == pm:
        if query.data == 'Off':
            users[userid]['AMPS'] = 'Off'
            users[userid]['PMPS'] = 'Off'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'Leave':
            users[userid]['AMPS'] = 'Leave'
            users[userid]['PMPS'] = 'Leave'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'MC':
            users[userid]['AMPS'] = 'MC'
            users[userid]['PMPS'] = 'MC'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="End Date?",
                                          reply_markup=telegramcalendar.create_calendar(), parse_mode=ParseMode.HTML)
            return ENTERDATE
        elif query.data == 'MA':
            users[userid]['AMPS'] = 'MA'
            users[userid]['PMPS'] = 'MA'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSO':
            users[userid]['AMPS'] = 'RSO'
            users[userid]['PMPS'] = 'RSO'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'RSI':
            users[userid]['AMPS'] = 'RSI'
            users[userid]['PMPS'] = 'RSI'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)
        elif query.data == 'AO':
            users[userid]['AMPS'] = 'AO'
            users[userid]['PMPS'] = 'AO'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'OS':
            users[userid]['AMPS'] = 'OS'
            users[userid]['PMPS'] = 'OS'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Location?", parse_mode=ParseMode.HTML)
            print("ENTERSTUFFFF")
            return ENTERSTUFF
        elif query.data == 'Course':
            users[userid]['AMPS'] = 'Course'
            users[userid]['PMPS'] = 'Course'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Course name?", parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Others':
            users[userid]['AMPS'] = 'Others'
            users[userid]['PMPS'] = 'Others'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            query.message.bot.sendMessage(chat_id=userid, text="Please enter your parade state.",
                                          parse_mode=ParseMode.HTML)
            return ENTERSTUFF
        elif query.data == 'Present':
            users[userid]['AMPS'] = 'Present'
            users[userid]['PMPS'] = 'Present'
            users[userid]['amtext'] = ""
            users[userid]['pmtext'] = ""
            paradestateEditMessage(Update, CallbackContext)


def paradestateEditMessage(update: Update, context: CallbackContext, ) -> None:
    global Totalstrength, Currentstrength, JurongCstrength, JurongTstrength, JurongLVE, JurongOFF, JurongMC, JurongOS, JurongAO, JurongOthers
    global JurongRSO, JurongRSI, JurongCourse, JurongMA, query
    global JLVE, JOFF, JMC, JOS, JAO, JOTHERS, JCourse, JMA, JRSO, JRSI, users, HQ, S1, S2, S3, am
    am = 0
    pm = 0
    keyboard = [
        [
            InlineKeyboardButton("AM", callback_data='AM'),
            InlineKeyboardButton("PM", callback_data='PM'),
        ],
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
    userdata = json.dumps(users)
    with open('user_data.json', 'w') as outfile:
        outfile.write(userdata)
    for x in users:
        if users[x]["Section"] == 'HQ':
            HQ = HQ + fr'{users[x]["Rank"]} {users[x]["Name"]}: '
            if users[x]["AMPS"] == users[x]["PMPS"] and users[x]["amtext"] == users[x]["pmtext"]:
                if users[x]["AMPS"] != "Others":
                    HQ = HQ + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present":
                    HQ = HQ + '\n'
                elif users[x]["AMPS"] == "MC" or users[x]["AMPS"] == "Leave" or users[x]["AMPS"] == "Off":
                    HQ = HQ + ' till ' + fr'{users[x]["enddate"]}' + '\n'
                elif users[x]["AMPS"] == "OS":
                    HQ = HQ + ' ' + fr'{users[x]["amtext"]}' + '\n'
                elif users[x]["AMPS"] == "AO" or users[x]["AMPS"] == "Others" or users[x]["AMPS"] == "Course":
                    HQ = HQ + ' ' + fr'{users[x]["amtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
            else:
                if users[x]["AMPS"] != "Others":
                    HQ = HQ + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present" or users[x]["AMPS"] == "Off" or users[x]["AMPS"] == "Leave":
                    HQ = HQ + "(AM) "
                elif users[x]["AMPS"] == "OS" or users[x]["AMPS"] == "Course" or users[x]["AMPS"] == "Others":
                    HQ = HQ + " " + fr'{users[x]["amtext"]}' + "(AM) "
                if users[x]["PMPS"] != "Others":
                    HQ = HQ + fr'{users[x]["PMPS"]}'
                if users[x]["PMPS"] == "MA" or users[x]["PMPS"] == "RSO" or users[x]["PMPS"] == "RSI" or users[x][
                    "PMPS"] == "Present":
                    HQ = HQ + "(PM)" + "\n"
                elif users[x]["PMPS"] == "OS":
                    HQ = HQ + ' ' + fr'{users[x]["pmtext"]}' + "(PM)" + '\n'
                elif users[x]["PMPS"] == "AO" or users[x]["PMPS"] == "Course" or users[x]["PMPS"] == "Others":
                    HQ = HQ + ' ' + fr'{users[x]["pmtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
        elif users[x]["Section"] == 'Section 1':
            S1 = S1 + fr'{users[x]["Rank"]} {users[x]["Name"]}: '
            if users[x]["AMPS"] == users[x]["PMPS"] and users[x]["amtext"] == users[x]["pmtext"]:
                if users[x]["AMPS"] != "Others":
                    S1 = S1 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present":
                    S1 = S1 + '\n'
                elif users[x]["AMPS"] == "MC" or users[x]["AMPS"] == "Leave" or users[x]["AMPS"] == "Off":
                    S1 = S1 + ' till ' + fr'{users[x]["enddate"]}' + '\n'
                elif users[x]["AMPS"] == "OS":
                    S1 = S1 + ' ' + fr'{users[x]["amtext"]}' + '\n'
                elif users[x]["AMPS"] == "AO" or users[x]["AMPS"] == "Others" or users[x]["AMPS"] == "Course":
                    S1 = S1 + ' ' + fr'{users[x]["amtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
            else:
                if users[x]["AMPS"] != "Others":
                    S1 = S1 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present" or users[x]["AMPS"] == "Off" or users[x]["AMPS"] == "Leave":
                    S1 = S1 + "(AM) "
                elif users[x]["AMPS"] == "OS" or users[x]["AMPS"] == "Course" or users[x]["AMPS"] == "Others":
                    S1 = S1 + " " + fr'{users[x]["amtext"]}' + "(AM) "
                if users[x]["PMPS"] != "Others":
                    S1 = S1 + fr'{users[x]["PMPS"]}'
                if users[x]["PMPS"] == "MA" or users[x]["PMPS"] == "RSO" or users[x]["PMPS"] == "RSI" or users[x][
                    "PMPS"] == "Present":
                    S1 = S1 + "(PM)" + "\n"
                elif users[x]["PMPS"] == "OS":
                    S1 = S1 + ' ' + fr'{users[x]["pmtext"]}' + "(PM)" + '\n'
                elif users[x]["PMPS"] == "AO" or users[x]["PMPS"] == "Course" or users[x]["PMPS"] == "Others":
                    S1 = S1 + ' ' + fr'{users[x]["pmtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'

        elif users[x]["Section"] == 'Section 2':
            S2 = S2 + fr'{users[x]["Rank"]} {users[x]["Name"]}: '
            if users[x]["AMPS"] == users[x]["PMPS"] and users[x]["amtext"] == users[x]["pmtext"]:
                if users[x]["AMPS"] != "Others":
                    S2 = S2 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present":
                    S2 = S2 + '\n'
                elif users[x]["AMPS"] == "MC" or users[x]["AMPS"] == "Leave" or users[x]["AMPS"] == "Off":
                    S2 = S2 + ' till ' + fr'{users[x]["enddate"]}' + '\n'
                elif users[x]["AMPS"] == "OS":
                    S2 = S2 + ' ' + fr'{users[x]["amtext"]}' + '\n'
                elif users[x]["AMPS"] == "AO" or users[x]["AMPS"] == "Others" or users[x]["AMPS"] == "Course":
                    S2 = S2 + ' ' + fr'{users[x]["amtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
            else:
                if users[x]["AMPS"] != "Others":
                    S2 = S2 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present" or users[x]["AMPS"] == "Off" or users[x]["AMPS"] == "Leave":
                    S2 = S2 + "(AM) "
                elif users[x]["AMPS"] == "OS" or users[x]["AMPS"] == "Course" or users[x]["AMPS"] == "Others":
                    S2 = S2 + " " + fr'{users[x]["amtext"]}' + "(AM) "
                if users[x]["PMPS"] != "Others":
                    S2 = S2 + fr'{users[x]["PMPS"]}'
                if users[x]["PMPS"] == "MA" or users[x]["PMPS"] == "RSO" or users[x]["PMPS"] == "RSI" or users[x][
                    "PMPS"] == "Present":
                    S2 = S2 + "(PM)" + "\n"
                elif users[x]["PMPS"] == "OS":
                    S2 = S2 + ' ' + fr'{users[x]["pmtext"]}' + "(PM)" + '\n'
                elif users[x]["PMPS"] == "AO" or users[x]["PMPS"] == "Course" or users[x]["PMPS"] == "Others":
                    S2 = S2 + ' ' + fr'{users[x]["pmtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
        elif users[x]["Section"] == 'Section 3':
            S3 = S3 + fr'{users[x]["Rank"]} {users[x]["Name"]}: '
            if users[x]["AMPS"] == users[x]["PMPS"] and users[x]["amtext"] == users[x]["pmtext"]:
                if users[x]["AMPS"]!="Others":
                    S3 = S3 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present":
                    S3 = S3 + '\n'
                elif users[x]["AMPS"] == "MC" or users[x]["AMPS"] == "Leave" or users[x]["AMPS"] == "Off":
                    S3 = S3 + ' till ' + fr'{users[x]["enddate"]}' + '\n'
                elif users[x]["AMPS"] == "OS":
                    S3 = S3 + ' ' + fr'{users[x]["amtext"]}' + '\n'
                elif users[x]["AMPS"] == "AO" or users[x]["AMPS"] == "Others" or users[x]["AMPS"] == "Course":
                    S3 = S3 + ' ' + fr'{users[x]["amtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
            else:
                if users[x]["AMPS"] != "Others":
                    S3 = S3 + fr'{users[x]["AMPS"]}'
                if users[x]["AMPS"] == "MA" or users[x]["AMPS"] == "RSO" or users[x]["AMPS"] == "RSI" or users[x][
                    "AMPS"] == "Present" or users[x]["AMPS"] == "Off" or users[x]["AMPS"] == "Leave":
                    S3 = S3 + "(AM) "
                elif users[x]["AMPS"] == "OS" or users[x]["AMPS"] == "Course" or users[x]["AMPS"] == "Others":
                    S3 = S3 + " " + fr'{users[x]["amtext"]}' + "(AM) "
                if users[x]["PMPS"] != "Others":
                    S3 = S3 + fr'{users[x]["PMPS"]}'
                if users[x]["PMPS"] == "MA" or users[x]["PMPS"] == "RSO" or users[x]["PMPS"] == "RSI" or users[x][
                    "PMPS"] == "Present":
                    S3 = S3 + "(PM)" + "\n"
                elif users[x]["PMPS"] == "OS":
                    S3 = S3 + ' ' + fr'{users[x]["pmtext"]}' + "(PM)" + '\n'
                elif users[x]["PMPS"] == "AO" or users[x]["PMPS"] == "Course" or users[x]["PMPS"] == "Others":
                    S3 = S3 + ' ' + fr'{users[x]["pmtext"]}' + ' till ' + fr'{users[x]["enddate"]}' + '\n'
        if users[x]["AMPS"] == "Off":
            JurongOFF += 1
        if users[x]["AMPS"] == "Leave":
            JurongLVE += 1
        if users[x]["AMPS"] == "MC":
            JurongMC += 1
        if users[x]["AMPS"] == "MA":
            JurongMA += 1
        if users[x]["AMPS"] == "RSO":
            JurongRSO += 1
        if users[x]["AMPS"] == "RSI":
            JurongRSI += 1
        if users[x]["AMPS"] == "AO":
            JurongAO += 1
        if users[x]["AMPS"] == "Course":
            JurongCourse += 1
        if users[x]["AMPS"] == "OS":
            JurongOS += 1
        if users[x]["AMPS"] == "Others":
            JurongOthers += 1
        if users[x]["AMPS"] == "Present":
            JurongCstrength += 1
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
    Totalstrength = JurongTstrength
    Currentstrength = JurongCstrength
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
        fr'{S3}', parse_mode='HTML', reply_markup=reply_markup

    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # add conv handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setup', setup), CommandHandler('start', setup)],
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
            EDITPS: [CallbackQueryHandler(paradestateEdit),
                     CommandHandler('endps', end)
                     ],
            ENTERSTUFF: [MessageHandler(Filters.text, getstuff)],
            ENTERDATE: [CallbackQueryHandler(getDate)],
        }, fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        per_chat=False
    )
    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler2)
    dispatcher.add_handler(CallbackQueryHandler(paradestateEdit))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
