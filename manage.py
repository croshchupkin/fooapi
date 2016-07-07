#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from oauth2client.service_account import ServiceAccountCredentials

from fooapi.app import create_app
from fooapi.models import db


manager = Manager(create_app)
manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def print_access_token(json_keyfile_path):
    scopes = manager.app.config['GOOGLE_API_SCOPES']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path,
                                                             scopes=scopes)
    print creds.get_access_token().access_token


if __name__ == '__main__':
    manager.run()
