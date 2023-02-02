import os
# from database import get_db

from flask import Flask
import mysql.connector as mysql


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

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

    @app.route('/')
    def index():
        return 'Game Swap Application'

    from . import db
    db.init_app(app)

    from . import gameswap
    app.register_blueprint(gameswap.bp)

    # from . import application
    # app.register_blueprint(application.bp)
    # app.add_url_rule('/', endpoint='index')

    return app