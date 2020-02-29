# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import sys
import slack
from credentials.keys import *

slack_key = keys["slack"]
server_users = keys["server_users"]

duration = sys.argv[1]

tars = slack.WebClient(slack_key)
tars.chat_postMessage(channel=server_users, text="Server down " + duration + ". Hopefully, we'll be back on soon.")
