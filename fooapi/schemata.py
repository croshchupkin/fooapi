# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate, decorators

from fooapi.models import Contact, User


class LimitOffsetSchema(Schema):
    limit = fields.Integer(missing=None, validate=validate.Range(min=1))
    offset = fields.Integer(missing=None, validate=validate.Range(min=1))


class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    phone_no = fields.String(missing='', validate=validate.Length(equal=13))
    email = fields.Email(missing='', validate=validate.Length(min=3))
    type_dumped = fields.Integer(
        missing=Contact.TYPE_OTHER,
        dump_only=True,
        dump_to='type',
        validate=validate.OneOf(Contact.TYPES_TO_NAMES.keys()))
    type_loaded = fields.String(
        missing=Contact.TYPES_TO_NAMES[Contact.TYPE_OTHER],
        load_only=True,
        load_to='type',
        validate=validate.OneOf(Contact.NAMES_TO_TYPES.keys()))

    @decorators.post_load
    def post_load(self, data):
        data['type'] = Contact.NAMES_TO_TYPES[data['type']]
        return data

    @decorators.post_dump
    def post_dump(self, data):
        data['type'] = Contact.TYPES_TO_NAMES[data['type']]
        return data
