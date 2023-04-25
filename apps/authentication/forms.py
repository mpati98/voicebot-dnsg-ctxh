# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    chatReq = StringField('ChatHistory',
                            id='req_record')
    chatResp = StringField('ChatHistory',
                            id='resp_record')
    createAt = StringField('CreateAt',
                            id='chat_time')

class CreateEventForm(FlaskForm):
    eventName = StringField('Event',
                         id='event_create',
                         validators=[DataRequired()])
    address = StringField('Address',
                      id='address_create',
                      validators=[DataRequired()])
    dateTime = StringField('Date',
                      id='date_create',
                      validators=[DataRequired()])
    content = StringField('Content',
                             id='content_create',
                             validators=[DataRequired()])
    notes = StringField('notes',
                            id='notes')
