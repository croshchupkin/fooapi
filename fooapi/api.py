# -*- coding: utf-8 -*-
from flask import request
from flask_restplus import Api, Resource
from marshmallow.validate import ValidationError
from oauth2client.client import AccessTokenCredentialsError

from fooapi.db_interaction import (
    get_users_list,
    get_single_user,
    add_user,
    update_user,
    delete_user,
    get_user_contacts_list,
    add_user_contact,
    delete_contact,
    delete_all_user_contacts,
    get_single_contact,
    update_contact)
from fooapi.auth_utils import (
    AccessDeniedException,
    UserProfileAccessException,
    get_email,
    ensure_can_edit_user,
    ensure_can_edit_contact)
from fooapi.schemata import (
    LimitOffsetSchema,
    UserSchema,
    ContactSchema,
    AccessTokenSchema)
from fooapi.models import Contact
from fooapi.utils import validation_errors_to_unicode_message


api = Api(prefix='/api')


# these parsers are here only for the purposes of Swagger UI generation
auth_parser = api.parser()
auth_parser.add_argument('X-Access-Token', type=str,location='headers')

user_parser = api.parser()
user_parser.add_argument('name', type=unicode, location='form')
user_parser.add_argument('X-Access-Token', type=str,location='headers')

contact_parser = api.parser()
contact_parser.add_argument('phone_no', type=str, location='form')
contact_parser.add_argument('email', type=str, location='form')
contact_parser.add_argument('type', type=str, location='form',
                            choices=Contact.NAMES_TO_TYPES.keys())
contact_parser.add_argument('X-Access-Token', type=str, location='headers')

list_parser = api.parser()
list_parser.add_argument('limit', type=int, location='args')
list_parser.add_argument('offset', type=int, location='args')


@api.route('/users', endpoint='api.users')
class Users(Resource):
    @api.doc(parser=list_parser)
    def get(self):
        res = LimitOffsetSchema().load(request.args)
        users, total = get_users_list(**res.data)
        return {
            'total': total,
            'results': UserSchema().dump(users, many=True).data
        }

    @api.doc(parser=user_parser)
    def post(self):
        form_res = UserSchema().load(request.form)
        header_res = AccessTokenSchema().load(request.headers)
        data = {}
        data.update(form_res.data)
        data['creator_email'] = get_email(header_res.data['x_access_token'])
        new_id = add_user(data)
        return {'result': {'user_id': new_id}}, 201


@api.route('/users/<int:user_id>/contacts', endpoint='api.contacts')
class UserContacts(Resource):
    @api.doc(parser=list_parser)
    def get(self, user_id):
        res = LimitOffsetSchema().load(request.args)
        contacts, total = get_user_contacts_list(user_id, **res.data)
        return {
            'total': total,
            'results': ContactSchema().dump(contacts, many=True).data
        }

    @api.doc(parser=contact_parser)
    def post(self, user_id):
        form_res = ContactSchema().load(request.form)
        header_res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_user(user_id, header_res.data['x_access_token'])
        new_id = add_user_contact(user_id, form_res.data)
        return {'result': {'contact_id': new_id}}, 201

    @api.doc(parser=auth_parser)
    def delete(self, user_id):
        res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_user(user_id, res.data['x_access_token'])
        delete_all_user_contacts(user_id)
        return '', 204


@api.route('/users/<int:user_id>', endpoint='api.single_user')
class SingleUser(Resource):
    def get(self, user_id):
        user = get_single_user(user_id)
        return {
            'result': UserSchema().dump(user).data
        }

    @api.doc(parser=user_parser)
    def put(self, user_id):
        form_res = UserSchema().load(request.form)
        header_res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_user(user_id, header_res.data['x_access_token'])
        update_user(user_id, form_res.data)
        return '', 204

    @api.doc(parser=auth_parser)
    def delete(self, user_id):
        res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_user(user_id, res.data['x_access_token'])
        delete_user(user_id)
        return '', 204


@api.route('/contacts/<int:contact_id>', endpoint='api.single_contact')
class SingleContact(Resource):
    def get(self, contact_id):
        contact = get_single_contact(contact_id)
        return {
            'result': ContactSchema().dump(contact).data
        }

    @api.doc(parser=contact_parser)
    def put(self, contact_id):
        form_res = ContactSchema().load(request.form)
        header_res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_contact(contact_id, header_res.data['x_access_token'])
        update_contact(contact_id, form_res.data)
        return '', 204

    @api.doc(parser=auth_parser)
    def delete(self, contact_id):
        res = AccessTokenSchema().load(request.headers)
        ensure_can_edit_contact(contact_id, res.data['x_access_token'])
        delete_contact(contact_id)
        return '', 204


@api.errorhandler(ValidationError)
def handle_validation_errors(e):
    # The ValidationError's `data` attribute clashes with the `data` attaribute
    # that flask_restplus.api.Api.handle_error() looks for, so if we don't
    # delete it here, the end response will not contain the correct information.
    del e.data
    return {'message': validation_errors_to_unicode_message(e.messages)}, 400


@api.errorhandler(AccessTokenCredentialsError)
def handle_credentials_errors(e):
    return {'message': e.message}, 401


@api.errorhandler(AccessDeniedException)
def handle_access_denied(e):
    return {'message': e.message}, 403


@api.errorhandler(UserProfileAccessException)
def handle_user_profile_access_error(e):
    return {'message': e.message}, 401
