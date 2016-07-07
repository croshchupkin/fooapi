# -*- coding: utf-8 -*-
import json

from flask import current_app as app
from oauth2client.client import AccessTokenCredentials
from httplib2 import Http

from db_interaction import get_single_user, get_single_contact


class AccessDeniedException(Exception):
    pass


def ensure_can_edit_user(user_id, access_token):
    pass


def ensure_can_edit_contact(contact_id, access_token):
    pass


def _get_email(access_token):
    creds = AccessTokenCredentials(access_token, 'fooapi/0.1')
    h = creds.authorize(Http())
    resp, content = h.request(app.config['GOOGLE_API_INFO_URL'])
    if resp['status'] != 200:
        raise AccessDeniedException('Unable to access the user profile.')

    data = json.loads(content)
    return  data['email']
