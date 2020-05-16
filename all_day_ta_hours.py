import slack
from credentials.keys import *
import datetime
import pyrebase

tars_token = keys["sfserver"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)
sf_ta = keys["sf_ta"]
ta_group = keys["ta_group"]

tars_fb_config = {
  "apiKey": keys["tars_fb_key"],
  "authDomain": keys["tars_fb_ad"],
  "databaseURL": keys["tars_fb_url"],
  "storageBucket": keys["tars_fb_sb"]
}
tars_fb = pyrebase.initialize_app(tars_fb_config)
db = tars_fb.database()

ts = open("credentials/message.txt", "r").read()
q = "*Teaching Assistant Hours for " + ts + "*"
poll = db.child(keys["key_fb_tars"]).child("polls").get().val()
poll = dict(zip(poll.keys(), poll.values()))
for key in poll.keys():
    value = poll[key]
    if value["message"][0]["text"]["text"] == q:
        poll = value
        ts = key.replace(".", "-")
        break
db.child(keys["key_fb_tars"]).child("polls").child(ts).remove()
text = q + "\n"
for block in poll["message"][1:-3]:
    try:
        text += block["text"]["text"].split("`")[0].strip() + " " + block["text"]["text"].split("`")[2] + "\n"
    except:
        text += block["text"]["text"] + "\n"
tars.chat_delete(channel=ta_group, ts=ts.replace("-", "."))
tars.chat_postMessage(channel=sf_ta, text=text)
tars.chat_postMessage(channel=keys["orientation_assignments"], text=text)
tars.chat_postMessage(channel=keys["orientation_project"], text=text)
tars.chat_postMessage(channel=keys["general"], text=text)

i = datetime.date.today().weekday() + 2
i = i % 7
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
message = tars.chat_postMessage(channel=ta_group, text="<@" + tars_id + "> poll \"Teaching Assistant Hours for " + days[i] + "\" \"11:00-12:30\" \"14:00-16:00\" \"16:00-18:00\" \"18:00-20:00\"", as_user=True)

with open("credentials/message.txt", "w") as f:
    f.write(days[i])
