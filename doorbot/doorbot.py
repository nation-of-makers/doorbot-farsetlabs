from flask import Flask, Response, request
from flask_sslify import SSLify
from flask.ext.httpauth import HTTPBasicAuth
from logbook import Logger
import json
import os.path

app = Flask(__name__)
sslify = SSLify(app)
auth = HTTPBasicAuth()
app.log = Logger(__name__)

user_db = json.load(
    open(os.path.expanduser("~/.doorbot_users"), 'r')
)

@auth.get_password
def get_pw(username):
    if username in user_db:
        return user_db.get(username)
    return None

config_settings = {
    'doors':[
        {'door_name':"Front Door",
         'doorid':"front",
        'interface': "piface",
        'interfaceopt':0},

        {'door_name':"Back Door",
         'doorid':"back",
        'interface': "piface",
        'interfaceopt':1},
    ]
}

import interfaces
app.doors = { 
    door_config['doorid']:interfaces.pick(
        door_config['interface']
    )(**door_config) for door_config in config_settings['doors']
}

app.log.debug("Got Doors: {} from Config {}".format(app.doors, config_settings))

import views