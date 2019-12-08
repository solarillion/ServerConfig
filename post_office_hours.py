import slack
from credentials.keys import *

tars_token = keys["slack"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)

tars.chat_postMessage(channel=tars_id, text="Post office hours.")
