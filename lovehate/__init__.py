import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_restful import Api


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
# rest_api = Api()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api.main import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .api.auth import api_bp as api_auth_bp
    app.register_blueprint(api_auth_bp, url_prefix='/api/auth')

    file_handler = RotatingFileHandler("lovehate.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)

    return app
