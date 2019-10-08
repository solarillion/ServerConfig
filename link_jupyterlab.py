# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import json
import requests
from slacker import Slacker
from credentials import *

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

r = requests.post("https://api.rebrandly.com/v1/links",
	data=json.dumps(link_request), headers=request_headers)
link = r.json()

slack = Slacker(keys["slack"])
slack.chat.post_message("#server_users", "JupyterHub: rebrand.ly/sf_jupyter or " + str(jupyterhub.json()["public_url"]) + "\nSSH: " + str(ssh.json()["public_url"]))
