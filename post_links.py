# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
import json
import requests
from slack_bolt import App
from credentials.keys import *

rebrandly_key = keys["rebrandly"]
jupyterhub_link_id = keys["jupyterhub"]
keeweb_link_id = keys["keeweb"]
slack_key = keys["slack"]
signing_secret = keys["signing_secret"]
server_users = keys["server_users"]

jupyterhub = requests.get("http://localhost:6001/api/tunnels/jupyterhub")
keeweb = requests.get("http://localhost:6001/api/tunnels/keeweb")
ssh = requests.get("http://localhost:6001/api/tunnels/ssh")

with open("/home/sfserver/post_links_request.txt", "w") as f:
    f.write(str(jupyterhub.json()))

jupyterhub_link_request = {
    "id": jupyterhub_link_id,
    "destination": jupyterhub.json()["public_url"],
    "title": "SF JupyterHub",
    "favourite": False,
    "shortUrl": "rebrand.ly/sf_jupyter",
}

keeweb_link_request = {
    "id": keeweb_link_id,
    "destination": keeweb.json()["public_url"],
    "title": "SF KeeWeb",
    "favourite": False,
    "shortUrl": "rebrand.ly/sf_keeweb",
}

request_headers = {"Content-type": "application/json", "apikey": rebrandly_key}

r = requests.post(
    "https://api.rebrandly.com/v1/links/" + str(jupyterhub_link_id),
    data=json.dumps(jupyterhub_link_request),
    headers=request_headers,
)
link = r.json()

r = requests.post(
    "https://api.rebrandly.com/v1/links/" + str(keeweb_link_id),
    data=json.dumps(keeweb_link_request),
    headers=request_headers,
)
link = r.json()

ssh_ngrok_port = ssh.json()["public_url"].split(":")[2]
ssh_ngrok_url = ssh.json()["public_url"].split(":")[1][2:]  # strip  the '//'

tars = App(token=slack_key, signing_secret=signing_secret)
tars.client.chat_postMessage(
    channel=server_users,
    text="And we're back on. *flashes cue light*­\nJupyterHub: "
    + str(jupyterhub.json()["public_url"])
    + "\nKeeWeb: "
    + str(keeweb.json()["public_url"])
    + "\nSSH: "
    + str(ssh.json()["public_url"])
    + "\nTo access the server over SSH, run\n`ssh USER@"
    + str(ssh_ngrok_url)
    + " -p"
    + ssh_ngrok_port
    + "`\nin your terminal, replacing USER with your server username.",
)
