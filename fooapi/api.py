# -*- coding: utf-8 -*-
from flask import request
from flask_restplus import Api
from flask_restplus import Resource

from fooapi.data_retrieval import (
    get_users_list)
from fooapi.schemata import LimitOffsetSchema, UserSchema, ContactSchema


api = Api()


@api.route('/users')
class Users(Resource):
    def get(self):
        res = LimitOffsetSchema().load(request.args)
        users, total = get_users_list(**res.data)
        return {
            'total': total,
            'results': users
        }

    def post(self):
        pass


@api.route('/users/<int:user_id>/contacts')
class UserContacts(Resource):
    def get(self, user_id):
        pass

    def post(self, user_id):
        pass

    def delete(self, user_id):
        pass


@api.route('/users/<int:user_id>')
class SingleUser(Resource):
    def get(self, user_id):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass


@api.route('/contacts/<int:contact_id>')
class SingleContact(Resource):
    def get(self, contact_id):
        pass

    def put(self, contact_id):
        pass

    def delete(self, contact_id):
        pass
