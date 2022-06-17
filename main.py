import os, sys 
import datetime
import sqlite3
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
#configs
from config import TOKEN
from config import STARTMSG
from config import HELPMSG
from config import AHELPMSG
from config import TOADMINSMSG
from config import HGNOTPERM
from config import NOMESSAGES
from config import ADMINS
from config import ADMINSID
from config import BANLIST
from config import GROUPID
from config import LOG
from config import DAYS
from config import ONDAYS
from config import EASTERS
#---------

s = []
stage = ""
day = 0
subjects = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
]

shedule = sqlite3.connect('shedule.sqlite')
cursor = shedule.cursor()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start']) #Init bot
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, STARTMSG)
    await logit(message, "/start")

@dp.message_handler(commands=['cancel']) #Init bot
async def process_start_command(message: types.Message):
    stage = ""
    day = 0
    await bot.send_message(message.chat.id, "Отмена")
    await logit(message, "/cancel")

@dp.message_handler(commands=['today']) #Get shedule for today
async def process_today_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        today = datetime.datetime.today().weekday();
        await bot.send_message(message.chat.id, "Вывожу расписание на " + ONDAYS[today])
        cursor.execute("SELECT * FROM shedule WHERE id = " + str(today) + " LIMIT 1;")
        records = cursor.fetchall()
        tosend = (DAYS[today] + ":")
        no = 0
        j = 0
        while j < 8:
            if not (records[0][j+1] == "" or records[0][j+1][0] == " "): tosend += ("\n" + str(j+1) + ": " + str(records[0][j+1]))
            else: no += 1
            j+=1
        if no == 8: await bot.send_message(message.chat.id, "Сегодня нет занятий")
        else: await bot.send_message(message.chat.id, tosend)
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['tomorrow']) #Get shedule for tomorrow
async def process_tomorrow_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        tomorrow = datetime.datetime.today().weekday() + 1
        await bot.send_message(message.chat.id, "Вывожу расписание на " + ONDAYS[tomorrow])
        cursor.execute("SELECT * FROM shedule WHERE id = " + str(tomorrow) + " LIMIT 1;")
        records = cursor.fetchall()
        tosend = (DAYS[tomorrow] + ":")
        no = 0
        j = 0
        while j < 8:
            if not (records[0][j+1] == "" or records[0][j+1][0] == " "): tosend += ("\n" + str(j+1) + ": " + str(records[0][j+1]))
            else: no += 1
            j+=1
        if no == 8: await bot.send_message(message.chat.id, "На завтра занятий нет")
        else: await bot.send_message(message.chat.id, tosend)
        await logit(message, "/tomorrow")
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['tday']) #Get shedule for three days
async def process_tday_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        today = datetime.datetime.today().weekday();
        await bot.send_message(message.chat.id, "Вывожу расписание на " + ONDAYS[today] + ", " + ONDAYS[today+1] + " и на " + ONDAYS[today+2])
        nodays = "На "
        isnodays = False
        i = 0
        while i < 3:
            cursor.execute("SELECT * FROM shedule WHERE id = " + str(today) + " LIMIT 1;")
            records = cursor.fetchall()
            tosend = (DAYS[today] + ":")
            no = 0
            j = 0
            while j < 8:
                if not (records[0][j+1] == "" or records[0][j+1][0] == " "): tosend += ("\n" + str(j+1) + ": " + str(records[0][j+1]))
                else: no += 1
                j+=1
            if no == 8:
                nodays += (ONDAYS[today] + ", ")
                isnodays = True
            else: await bot.send_message(message.chat.id, tosend)
            i+=1
            if today < 6: today += 1
            else: today = 0
        inodays = "";
        if isnodays: 
            i = 0
            while i < (len(nodays) - 2):
                inodays += nodays[i]
                i += 1
            await bot.send_message(message.chat.id, (inodays + " нет занятий"))
        await logit(message, "/tday")
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['week']) #Get shedule for a week
async def process_week_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        await bot.send_message(message.chat.id, "Вывожу расписание на всю неделю")
        nodays = "На "
        isnodays = False
        i = 0
        while i < 7:
            cursor.execute("SELECT * FROM shedule WHERE id = " + str(i) + " LIMIT 1;")
            records = cursor.fetchall()
            tosend = (DAYS[i] + ":")
            no = 0
            j = 0
            while j < 8:
                if not (records[0][j+1] == "" or records[0][j+1][0] == " "): tosend += ("\n" + str(j+1) + ": " + str(records[0][j+1]))
                else: no += 1
                j+=1
            if no == 8:
                nodays += (ONDAYS[i] + ", ")
                isnodays = True
            else: await bot.send_message(message.chat.id, tosend)
            i+=1
        inodays = "";
        if isnodays: 
            i = 0
            while i < (len(nodays) - 2):
                inodays += nodays[i]
                i += 1
            await bot.send_message(message.chat.id, (inodays + " нет занятий"))
        await logit(message, "/week")
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['usersend']) #Send message to admins
async def process_usersend_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        await bot.send_message(message.chat.id, "Введите сообщение")
        global stage
        stage = "usersend"
        await logit(message, "/usersend")
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['help']) #Help
async def process_help_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        await bot.send_message(message.chat.id, HELPMSG)
        await logit(message, "/help")
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['as']) #Admin set shedule
async def process_as_command(message: types.Message):
    if await userStatus(message.from_user.username) == 2:
        await logit(message, "/as(ADMIN)")
        global stage
        if not (stage == "as" or stage == "sa"): 
            await bot.send_message(message.chat.id, "Выберите день недели (1-7)")
            stage = "as"
        elif stage == "sa":
            global day 
            await bot.send_message(message.chat.id, "Введите расписание на " + ONDAYS[day] + ", разделяя предметы запятой")
    else:
        await logit(message, "/as(NOT ADMIN)")
        await bot.send_message(message.chat.id, HGNOTPERM)
    
@dp.message_handler(commands=['aa']) #Admin add
async def process_aa_command(message: types.Message):
    if await userStatus(message.from_user.username) == 2:
        await logit(message, "/aa(ADMIN)")
        stage = "aa"
        await bot.send_message(message.chat.id, "Введите username пользователя, которого вы хотите повысить до администратора")
    else:
        await logit(message, "/aa(NOT ADMIN)")
        await bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['ab']) #Admin ban user
async def process_ab_command(message: types.Message):
    if await userStatus(message.from_user.username) == 2:
        await logit(message, "/ab(ADMIN)")
        stage = "ab"
        await bot.send_message(message.chat.id, "Введите username пользователя, которого вы хотите добавить в черный список")
    else:
        await logit(message, "/ab(NOT ADMIN)")
        await bot.send_message(message.chat.id, NOTANADMIN)

@dp.message_handler(commands=['au']) #Admin unban user
async def process_au_command(message: types.Message):
    if await userStatus(message.from_user.username) == 2:
        await logit(message, "/au(ADMIN)")
        stage = "au"
        await bot.send_message(message.chat.id, "Введите username пользователя, которого вы хотите удалить из черного списка")
    else:
        await logit(message, "/au(NOT ADMIN)")
        await bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['ams']) #Admin mail send
async def process_ams_command(message: types.Message):
    if await userStatus(message.from_user.username) == 2:
        await logit(message, "/ams(ADMIN)")
        await bot.send_message(message.chat.id, "Откройте личный чат, чтобы выполнить команду")
        await bot.send_message(message.from_user.id, "Введите сообщение")
        global stage
        stage = "ams"
    else:
        await logit(message, "/ams(NOT ADMIN)")
        await bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler(commands=['ah']) #Admin help
async def process_ah_command(message: types.Message):
    if not await userStatus(message.from_user.username) == 0:
        await logit(message, "/ah")
        await bot.send_message(message.chat.id, AHELPMSG)
    else: bot.send_message(message.chat.id, HGNOTPERM)

@dp.message_handler()
async def echo_message(msg: types.Message):
    if not await userStatus(msg.from_user.username) == 0:
        global stage
        global day
        if stage == "usersend":
            print(msg.text == "id1123356234")
            if msg.text == "id1123356234": await bot.send_message(msg.chat.id, EASTERS[random.randint(0,len(EASTERS))])
            else:
                stage = ""
                i = 0
                while i < len(ADMINSID):
                    await bot.send_message(ADMINSID[i], "@" + msg.from_user.username + TOADMINSMSG + msg.text + " - " + str(datetime.datetime.now()) + "\n")
                    i+=1
        elif stage == "ams":
            await bot.send_message(GROUPID, msg.text)
            stage = ""
        elif stage == "as":
            day = (int(msg.text)-1)
            stage = "sa"
            await process_as_command(msg)
        elif stage == "sa":
            global s
            s = [str(number) for number in msg.text.split(',')]
            #(1,2,3,4,5,6,7,8) * 7
            cursor.execute("SELECT EXISTS(SELECT * FROM shedule where id = "+str(day)+")")
            if cursor.fetchall(): cursor.execute("UPDATE shedule SET s1='"+s[0]+"',s2='"+s[1]+"',s3='"+s[2]+"',s4='"+s[3]+"',s5='"+s[4]+"',s6='"+s[5]+"',s7='"+s[6]+"',s8='"+s[7]+"' WHERE id = "+str(day)+";")
            else: cursor.execute("INSERT INTO shedule (id,s1,s2,s3,s4,s5,s6,s7,s8) VALUES ("+str(day)+",'"+s[0]+"','"+s[1]+"','"+s[2]+"','"+s[3]+"','"+s[4]+"','"+s[5]+"','"+s[6]+"','"+s[7]+"');")
            shedule.commit()
            stage = ""
        elif stage == "ab": cursor.execute("INSERT INTO users (id,username,status) VALUES (Null,'"+msg.text+"',0);")
        elif stage == "au": cursor.execute("INSERT INTO users (id,username,status) VALUES (Null,'"+msg.text+"',1);")
        elif stage == "aa": cursor.execute("INSERT INTO users (id,username,status) VALUES (Null,'"+msg.text+"',2);")
        
        if stage == "ab" or stage == "au" or stage == "aa": shedule.commit()
        await logit(msg, str(msg.text))
    else: bot.send_message(message.chat.id, HGNOTPERM)

async def logit(msg, ulog):
    log = "id" + str(msg.from_user.id) + " or " + msg.from_user.full_name + " or " + msg.from_user.username + " writed: '" + ulog + "' in " + str(datetime.datetime.now())
    f = open(LOG,"a")
    f.write(log + "\n")
    f.close()

async def userStatus(username):
    cursor.execute("SELECT status FROM users WHERE username = '" + username + "';")
    records = cursor.fetchall()
    return records[0][0]
    
if __name__ == '__main__':
    print("Bot has been started")
    executor.start_polling(dp)

shedule.close()