# -*- coding: utf-8 -*-
import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}/fooapi.db'.format(
    path=os.path.expanduser('~'))
