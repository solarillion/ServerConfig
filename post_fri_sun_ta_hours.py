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
friday = next_weekday(today, 4)
sunday = next_weekday(friday, 6)

tars_token = keys["slack"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)

sf_ta = keys["sf_ta"]
orientation_assignments = keys["orientation_assignments"]
orientation_project = keys["orientation_project"]

config = {
  "apiKey": keys["tars_fb_key"],
  "authDomain": keys["tars_fb_ad"],
  "databaseURL": keys["tars_fb_url"],
  "storageBucket": keys["tars_fb_sb"]
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
k = keys["key_fb_tars"]

fri_sun_poll = db.child(k).child("tapoll").child("frisun").get().val()
poll = db.child(k).child("polls").child(fri_sun_poll).get().val()
db.child(k).child("polls").child(fri_sun_poll).remove()

text = "TA Hours for Friday (" + friday.strftime("%d-%m-%Y") + ") through Sunday (" + sunday.strftime("%d-%m-%Y") + ") :\n"
for block in poll["message"][1:-3]:
	try:
		text += block["text"]["text"].split("`")[0].strip() + " " + block["text"]["text"].split("`")[2] + "\n"
	except:
		text += block["text"]["text"] + "\n"

tars.chat_delete(channel=sf_ta, ts=fri_sun_poll.replace("-", "."))
tars.chat_postMessage(channel=sf_ta, text=text)
tars.chat_postMessage(channel=orientation_assignments, text=text)
tars.chat_postMessage(channel=orientation_project, text=text)
tars.chat_postMessage(channel=general, text=text)
