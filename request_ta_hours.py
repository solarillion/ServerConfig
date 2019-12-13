import slack
import pyrebase
import datetime
from credentials.keys import *

def next_weekday(d, weekday):
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0:
		days_ahead += 7
	return d + datetime.timedelta(days_ahead)
today = datetime.date.today()
monday = next_weekday(today, 0)
sunday = next_weekday(monday, 6)

tars_token = keys["slack"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)

sf_ta = keys["sf_ta"]
tars.chat_postMessage(channel=sf_ta, text="Week " + monday.strftime("%d-%m-%Y") + " through " + sunday.strftime("%d-%m-%Y") + ":")
tars.chat_postMessage(channel=sf_ta, text="<@" + tars_id + "> poll \"Mon-Thu TA Hours\" \"Monday 18:00-20:00\" \"Tuesday 18:00-20:00\" \"Wednesday 18:00-20:00\" \"Thursday 18:00-20:00\"")
tars.chat_postMessage("Mark your hours by 18:00 on Sunday for Monday through Thursday.")
tars.chat_postMessage(channel=sf_ta, text="<@" + tars_id + "> poll \"Fri-Sun TA Hours\" \"Friday 18:00-20:00\" \"Saturday 13:00-15:00\" \"Saturday 16:00-18:00\" \"Saturday 18:00-20:00\" \"Sunday 10:30-13:00\" \"Sunday 13:30-16:00\" \"Sunday 16:30-19:00\"")
tars.chat_postMessage("Mark your hours by 18:00 on Thursday for Friday through Sunday.")
