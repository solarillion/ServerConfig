import slack
from credentials.keys import *
import time

tars_token = keys["slack"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)

tars.chat_postMessage(channel=tars_id, text="Wake up!")
time.sleep(10)
tars.chat_postMessage(channel=tars_id, text="Request office hours.")
