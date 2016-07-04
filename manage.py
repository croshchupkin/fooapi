#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server

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


if __name__ == '__main__':
    manager.run()
