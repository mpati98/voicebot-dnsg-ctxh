# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import sqlite3
import pandas as pd

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

# get chat history
@blueprint.route('/chat-history', methods=['GET', 'POST'])
@login_required
def view_history():
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("apps/db.sqlite3")
    df = pd.read_sql_query("SELECT * from Users", con)
    df = df.drop(['email', 'password', 'oauth_github'], axis=1)

    column_name = list(df.columns)
    all_values = df.values
    numOfRow = df.shape[0]
    # Be sure to close the connection
    con.close()
    return render_template('home/chatHistory.html',column_name = column_name, all_values = all_values, numOfRow = numOfRow)

@blueprint.route('/chat-history/<int:userid>', methods=['GET', 'POST'])
@login_required
def view_history_detail(userid):
    print(type(userid))
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("apps/db.sqlite3")
    df = pd.read_sql_query("SELECT * from Users", con)
    df = df.drop(['email', 'password', 'oauth_github'], axis=1)

    chat_value = df.values[int(userid)]
    user_name = chat_value[1]
    cus_req = chat_value[2].split(';')
    bot_req = chat_value[3].split(';')
    numOfChat = len(cus_req)
    # Be sure to close the connection
    con.close()
    return render_template('home/historyDetail.html',user_name = user_name, cus_req = cus_req, bot_req = bot_req, numOfChat = numOfChat)

# get chat history
@blueprint.route('/member', methods=['GET', 'POST'])
@login_required
def view_member():
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("apps/db.sqlite3")
    df = pd.read_sql_query("SELECT * from Users", con)
    df = df.drop(['email', 'password', 'oauth_github'], axis=1)

    column_name = list(df.columns)
    all_values = df.values
    numOfRow = df.shape[0]
    # Be sure to close the connection
    con.close()
    return render_template('home/member.html',column_name = column_name, all_values = all_values, numOfRow = numOfRow)