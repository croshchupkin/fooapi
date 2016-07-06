# -*- coding: utf-8 -*-
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import utils


db = SQLAlchemy()


class SetFieldsMixin(object):
    def set_fields(self, data):
        for name, val in data.iteritems():
            setattr(name, val)


class Contact(db.Model, SetFieldsMixin):
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
    phone_no = db.Column(db.String(30), default=None)
    email = db.Column(db.String(128), default=None)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True,
                           nullable=False)
    type = db.Column(db.SmallInteger(), nullable=False, default=TYPE_OTHER)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey(
                            'users.id',
                            ondelete='CASCADE'),
                        nullable=False)

    def __repr__(self):
        return ('<Contact id={id}, phone_no={phone}, email={email}, '
                'type={type}, created_at={created_at}>').format(
                    id=self.id,
                    phone=self.phone_no,
                    email=self.email,
                    type=self.TYPES_TO_NAMES[self.type],
                    created_at=utils.isoformat(self.created_at))


class User(db.Model, SetFieldsMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(128), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True,
                           nullable=False)
    contacts = db.relationship('Contact', backref='user',
                               order_by=Contact.created_at,
                               cascade='all, delete-orphan',
                               passive_deletes=True)

    def __repr__(self):
        return ('<User id={id}, name={name}, created_at={created_at}, '
                'contacts=[{contacts}]>').format(
                    id=self.id,
                    name=self.name,
                    created_at=utils.isoformat(self.created_at),
                    contacts=', '.join((repr(c) for c in self.contacts)))
