# -*- coding: utf-8 -*-
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import *
from modules.settings import userdb, table, SECRET_KEY

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        )#DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import auth
    app.register_blueprint(auth.bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = userdb
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from . import search
    app.register_blueprint(search.bp)
    app.add_url_rule('/', endpoint='index')

    from . import db
    db.dbase.init_app(app)
    db.init_app(app)
    return app
