# -*- coding: utf-8 -*-
from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(128), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow,index=True,
                           nullable=False)


class Contact(db.Model):
    __tablename__ = 'contacts'

    TYPE_HOME = 1
    TYPE_WORK = 2
    TYPE_OTHER = 3
    TYPES_TO_NAMES = {
        TYPE_HOME: 'home',
        TYPE_WORK: 'work',
        TYPE_OTHER: 'other'
    }
    NAMES_TO_TYPES = {v:k for k,v in TYPES_TO_NAMES.iteritems()}

    id = db.Column(db.Integer(), primary_key=True)
    phone_no = db.Column(db.String(13), nullable=False, default='')
    email = db.Column(db.String(128), nullable=False, default='')
    type = db.Column(db.SmallInteger(), nullable=False)
    user = db.relationship('User', backref=db.backref('contacts'),
                           lazy='dynamic')
