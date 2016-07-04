# -*- coding: utf-8 -*-
from flask.ext.restplus import Api
from flask.ext.restplus import Resource


api = Api()


@api.route('/users')
class Users(Resource):
    def get(self):
        pass

    def post(self):
        pass


@api.route('/users/<int:user_id>/contacts')
class UserContacts(Resource):
    def get(self, user_id):
        pass

    def post(self, user_id):
        pass


@api.route('/users/<int:user_id>')
class SingleUser(Resource):
    def get(self, user_id):
        pass

    def put(self, user_id):
        pass


@api.route('/contacts/<int:contact_id>')
class SingleContact(Resource):
    def get(self, contact_id):
        pass

    def put(self, contact_id):
        pass
