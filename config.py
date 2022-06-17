TOKEN = "" #http token

GROUPID = -999999999999 #linked group

#Messages
STARTMSG = "" #start message
HELPMSG = "" #help message
AHELPMSG = "" #admin help message
HGNOTPERM = "" #have not got needed permissions (banned or not admin)
NOMESSAGES = "" #no messages to admins
TOADMINSMSG = " sent message: "
i = 0
while i < len(ADMINS):
    if i+1 != len(ADMINS):
        HELPMSG += ("@" + ADMINS[i] + ", ")
        AHELPMSG += ("@" + ADMINS[i] + ", ")
    else:
        HELPMSG += ("@" + ADMINS[i])
        AHELPMSG += ("@" + ADMINS[i])
    i+=1

LOG = "log.txt" #log file

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thurday",
    "Friday",
    "Saturday",
    "Sunday"
]
ONDAYS = [
    "moday",
    "tuesday",
    "wednesday",
    "thurday",
    "friday",
    "saturday",
    "sunday"
]

EASTERS = [
    "Easter egg"
]
