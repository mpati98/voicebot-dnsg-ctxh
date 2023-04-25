# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
from apps.authentication.models import Users, request_loader
from flask_migrate import Migrate
from sys import exit

from apps.config import config_dict
from apps import create_app, db
from flask import Flask, render_template, jsonify, request
from utils import transText, SpeakText, save_error, tts_fptAI, play_mp3, event_response
from pairAI.core.agents import create_agent_from_model_file
from chat import get_response
import random
import json
from os.path import exists
import speech_recognition as sr
import datetime
from flask_login import current_user, login_required
from apps.authentication.models import Users
import sqlite3
import pandas as pd
import requests

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)             )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT = ' + app_config.ASSETS_ROOT )


# app = Flask(__name__)
url = 'https://api.fpt.ai/hmi/tts/v5'
payload = ''
headers = {
    'api-key': 'OaGgkRmCMzOoZbnwgX70IDWo77t0g5SW',
    'speed': '',
    'voice': 'banmai'
}

def Model_init():
    # import model from the model file can be pretrained or fine tuned

    blender_agent = create_agent_from_model_file(
        "zoo:blender/blender_90M/model")
    return blender_agent

# function to add to JSON
def write_json(new_data, filename='ERROR_sample.json'):
    # Table column:
    # id
    # destination id
    # content
    # createAt
    
    with open(filename,'r+', encoding='utf-8') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat_history"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, ensure_ascii=False)

@app.route('/', methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route('/welcome', methods=["POST"])
def voice_welcome():
    welcome = "Xin chào, tôi là trợ lý ảo Ban công tác xã hội của câu lạc bộ Doanh nhân Sài Gòn, tôi có thẻ giúp gì cho bạn?"
    # SpeakText(welcome)
    audio = tts_fptAI(welcome)
    play_mp3(audio)
    return jsonify(welcome)

@app.route('/voice_predict', methods=["POST"])
def voice_predict():
    text_input = request.get_json().get("message")
    if text_input is None:
        text_to_sys = "Some thing wrong!"
        text_input = "tín hiệu không tốt"
    else:
        print(text_input)
        text_to_sys = transText(text_input, scr_input="user")
    try:
        resp, tag = get_response(text_to_sys)
        if tag == 'unknown_response':
            blender_agent.observe({'text': text_to_sys, 'episode_done': False})
            response = blender_agent.act()  # From bot
            res = transText(response['text'], scr_input="bot")
            # tts_fptAI(res)
            # SpeakText(res)
        else:
            res = event_response(tag=tag)
            if res == "None":
                res = random.choice(resp)
            # SpeakText(res)
            print(res)
    except:
        res = "Tôi không hiểu ý bạn lắm, phiền bạn giải thích rõ hơn nhé!"
        save_error('Chat basic mode error', 'chat_basic')
        data_dict = {"req": text_input, "resp": res}
        write_json(data_dict, filename="ERROR" + "_sample.json")
    message = {"answer": res}
    if current_user.chatReq:
        current_user.chatReq = current_user.chatReq + ';' + text_input
        current_user.chatResp = current_user.chatResp + ';' + res
    else:
        current_user.chatReq = text_input
        current_user.chatResp = res 
        current_user.createAt = datetime.datetime.now()
    db.session.add(current_user)
    db.session.commit()
    db.session.close()
    audio = tts_fptAI(res)
    play_mp3(audio)
    print("Input: ",text_input)
    print("Output: ", message["answer"])
    return jsonify(message)

@app.route('/predict', methods=["POST"])
def predict():
    text_input = request.get_json().get("message")
    text_to_sys = transText(text_input, scr_input="user")
    # print(text_to_sys)
    try:
        resp, tag = get_response(text_to_sys)
        if tag == "unknown_response":
            blender_agent.observe({'text': text_to_sys, 'episode_done': False})
            response = blender_agent.act()  # From bot
            res = transText(response['text'], scr_input="bot")
        else:
            res = random.choice(resp)
            # message = {"answer": res}
    except:
        res = "Tôi không hiểu ý bạn lắm, phiền bạn giải thích rõ hơn nhé!"
        save_error('Chat basic mode error', 'chat_basic')
        data_dict = {"req": text_input, "resp": res}
        write_json(data_dict, filename="ERROR" + "_sample.json")
    message = {"answer": res}
    print(res)
    if current_user.chatReq:
        current_user.chatReq = current_user.chatReq + ';' + text_input
        current_user.chatResp = current_user.chatResp + ';' + res
    else:
        current_user.chatReq = text_input
        current_user.chatResp = res
        current_user.createAt = datetime.datetime.now()
    db.session.add(current_user)
    db.session.commit()
    db.session.close()
    return jsonify(message)

if __name__ == "__main__":
    blender_agent = Model_init()
    app.run(debug=True, port=5000)
