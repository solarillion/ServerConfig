# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import json
import requests
from slacker import Slacker
from credentials.keys import *

rebrandly_key = keys["rebrandly"]
link_id = keys["link"]
slack_key = keys["slack"]

jupyterhub = requests.get("http://localhost:6001/api/tunnels/jupyterhub")
ssh = requests.get("http://localhost:6001/api/tunnels/ssh")

link_request = {
  "id": link_id,
  "destination": jupyterhub.json()["public_url"],
  "title": "SF JupyterHub",
  "favourite": False,
  "shortUrl": "rebrand.ly/sf_jupyter"
}

request_headers = {
  "Content-type": "application/json",
  "apikey": rebrandly_key
}

r = requests.post("https://api.rebrandly.com/v1/links/" + str(link_id),
	data=json.dumps(link_request), headers=request_headers)
link = r.json()

slack = Slacker(slack_key)
slack.chat.post_message("#server_users", "And we're back on. *flashes cue light*­\nJupyterHub: " + str(jupyterhub.json()["public_url"]) + "\nSSH: " + str(ssh.json()["public_url"]) + "\nVisit rebrand.ly/sf_jupyter for JupyterHub.")
