# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import sys
from slack_bolt import App
from credentials.keys import *

tars_token = keys["slack"]
tars_secret = keys["signing_secret"]
tars = App(token=tars_token, signing_secret=tars_secret)
server_users = keys["server_users"]

duration = sys.argv[1]

tars.client.chat_postMessage(
    channel=server_users,
    text="Server down " + duration + ". Hopefully, we'll be back on soon.",
)
