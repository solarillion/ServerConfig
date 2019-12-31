import slack
from credentials.keys import *

tars_token = keys["slack"]
tars_id = keys["tars"]
tars = slack.WebClient(token=tars_token)

sf_ta = keys["sf_ta"]
tars.chat_postMessage(channel=sf_ta, text="Don't forget to mark your Fri-Sun TA Hours before 9 AM, Thursday.")
