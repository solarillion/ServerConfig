# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import json
import requests
import slack
from credentials.keys import *

rebrandly_key = keys["rebrandly"]
jupyterhub_link_id = keys["jupyterhub"]
kronos_link_id = keys["kronos"]
slack_key = keys["slack"]
server_users = keys["server_users"]

jupyterhub = requests.get("http://localhost:6001/api/tunnels/jupyterhub")
kronos = requests.get("http://localhost:6001/api/tunnels/kronos")
ssh = requests.get("http://localhost:6001/api/tunnels/ssh")

jupyterhub_link_request = {
  "id": jupyterhub_link_id,
  "destination": jupyterhub.json()["public_url"],
  "title": "SF JupyterHub",
  "favourite": False,
  "shortUrl": "rebrand.ly/sf_jupyter"
}

kronos_link_request = {
  "id": kronos_link_id,
  "destination": kronos.json()["public_url"],
  "title": "SF Kronos",
  "favourite": False,
  "shortUrl": "rebrand.ly/sf_kronos"
}

request_headers = {
  "Content-type": "application/json",
  "apikey": rebrandly_key
}

r = requests.post("https://api.rebrandly.com/v1/links/" + str(jupyterhub_link_id), data=json.dumps(jupyterhub_link_request), headers=request_headers)
link = r.json()

r = requests.post("https://api.rebrandly.com/v1/links/" + str(kronos_link_id), data=json.dumps(kronos_link_request), headers=request_headers)
link = r.json()

ssh_ngrok_port = ssh.json()["public_url"].split(":")[2]

tars = slack.WebClient(slack_key)
tars.chat_postMessage(channel=server_users, text="And we're back on. *flashes cue light*­\nJupyterHub: " + str(jupyterhub.json()["public_url"]) + "\nVisit rebrand.ly/sf_jupyter to access JupyterHub.\nKronos: " + str(kronos.json()["public_url"]) + "\nVisit rebrand.ly/sf_kronos to access Kronos.\nSSH: "+ str(ssh.json()["public_url"]) + "\nTo access the server over SSH, run\n`ssh USER@0.tcp.ngrok.io -p" + ssh_ngrok_port +"`\nin your Terminal, replacing USER with your server username.")
