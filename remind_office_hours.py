from slack_bolt import App
from credentials.keys import *

tars_user_token = keys["sfserver"]
tars_id = keys["tars"]
tars_secret = keys["signing_secret"]

tars = App(
	token=tars_user_token,
	signing_secret=tars_secret
)

tars.client.chat_postMessage(channel=tars_id, text="remind office hours")
