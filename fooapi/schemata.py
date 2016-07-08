# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate, decorators
import phonenumbers

from fooapi.models import Contact


class PhoneNumber(validate.Validator):
    def __call__(self, value):
        # skip empty values (to allow us to clear the phone value)
        if not len(value):
            return value

        try:
            num = phonenumbers.parse(value)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise validate.ValidationError(e.message)

        if not phonenumbers.is_possible_number(num):
            raise validate.ValidationError('Such phone number is impossible.')

        return value


class Email(validate.Email):
    """
    Same as marshmallow's Email validator, but allows empty strings.
    """
    def __call__(self, value):
        if not len(value):
            return value
        return super(Email, self).__call__(value)


class LimitOffsetSchema(Schema):
    limit = fields.Integer(missing=None, validate=validate.Range(min=1))
    offset = fields.Integer(missing=None, validate=validate.Range(min=1))


class AccessTokenSchema(Schema):
    x_access_token = fields.String(load_only=True, required=True, validate=validate.Length(min=1))

    class Meta(object):
        strict = True


class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    phone_no = fields.String(
        required=True,
        validate=(validate.Length(max=30), PhoneNumber()))
    email = fields.String(
        required=True,
        validate=(validate.Length(max=128), Email()))
    type_dumped = fields.Integer(
        dump_only=True,
        attribute='type',
        dump_to='type',
        validate=validate.OneOf(Contact.TYPES_TO_NAMES.keys()))
    type = fields.String(
        required=True,
        load_only=True,
        validate=validate.OneOf(Contact.NAMES_TO_TYPES.keys()))

    class Meta(object):
        ordered = True
        strict = True

    @decorators.validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data):
        if not len(data['email'].strip()) and not len(data['phone_no'].strip()):
            raise validate.ValidationError(
                'A value must be provided for at least one of email and phone_no.')

    @decorators.post_load
    def post_load(self, data):
        """
        Converts the type's name to type's integer constant right after the
        load, because we represent the contact types as an easily understandable
        text in the API results and when handling POST/PUT requests, but in the
        end, when we work with database models, we want the type to be and int,
        so that it could be properly saved to DB.

        Also, strips leading and trailing whitespace from the string fields.
        """
        data['type'] = Contact.NAMES_TO_TYPES[data['type']]

        fields_to_strip = ('phone_no', 'email')
        for name in fields_to_strip:
            data[name] = data[name].strip()

        return data

    @decorators.post_dump
    def post_dump(self, data):
        """
        Converts the numeric type to textual right after the dump, because
        the model instances contain only the int value of type, and we want to
        nicely show this as text in the JSON returned by the API endpoints.
        """
        data['type'] = Contact.TYPES_TO_NAMES[data['type']]
        return data


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(min=1, max=128),
                         required=True)
    created_at = fields.DateTime(format='iso', dump_only=True)
    contacts = fields.Nested(ContactSchema, many=True, dump_only=True)

    class Meta(object):
        ordered = True
        strict = True

    @decorators.post_load
    def post_load(self, data):
        data['name'] = data['name'].strip()
        return data
