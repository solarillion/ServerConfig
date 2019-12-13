# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import pickle as pkl
import slack
import pyrebase
from credentials.keys import *

tars_token = keys["slack"]
tars = slack.WebClient(token=tars_token)

tars_fb_config = {
  "apiKey": keys["tars_fb_key"],
  "authDomain": keys["tars_fb_ad"],
  "databaseURL": keys["tars_fb_url"],
  "storageBucket": keys["tars_fb_sb"]
}
tars_fb = pyrebase.initialize_app(tars_fb_config)

tars_db = tars_fb.database()

all_users = tars.users_list().data["members"]
with open("credentials/all_users.pkl", "wb") as f:
    pkl.dump(all_users, f)

tas = []
orientees = []
groups = tars.groups_list().data["groups"]
for group in groups:
    if group["id"] == keys["sf_ta"]:
        tas = group["members"]
    if group["id"] == keys["orientation_assignments"] or group["id"] == keys["orientation_project"]:
        orientees += group["members"]

tas = set(tas)
current_orientees = set(tars_db.child(keys["key_fb_tars"]).child("orientee").get().val())
orientees = set(orientees)
orientees -= tas
orientees -= current_orientees

orientees_not_added = []
for i in orientees:
    orientees_not_added.append(tars.users_info(user=i).data["user"]["profile"]["real_name"])

tars_db.child(keys["key_fb_tars"]).child("ta").remove()
for i in tas:
    tars_db.child(keys["key_fb_tars"]).child("ta").update({str(i): str(tars.users_info(user=i).data["user"]["profile"]["real_name"])})

tars.chat_postMessage(channel=keys["tars_admin"], text="Orientees who haven't been added to the database: " + str(orientees_not_added))
