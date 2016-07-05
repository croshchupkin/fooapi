# -*- coding: utf-8 -*-
import os

from flask import Flask


def create_app(
        config_module='fooapi.settings',
        additional_config_envvar_name='FOOAPI_ADDITIONAL_SETTINGS_PATH'):
    app = Flask('fooapi')
    app.config.from_object(config_module)
    if additional_config_envvar_name in os.environ:
        app.config.from_envvar(additional_config_envvar_name)

    _init_db(app)
    _init_api(app)
    return app


def _init_db(app):
    from fooapi.models import db
    db.init_app(app)


def _init_api(app):
    from fooapi.api import api
    api.ui = app.config['ENABLE_SWAGGER_UI']
    api.init_app(app)
