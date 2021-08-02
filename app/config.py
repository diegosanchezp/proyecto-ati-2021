"""
Archivo de configuración de flask
"""
import os
from flask import url_for
class Config:
    """
    Clase de principal configuracion de flask
    """
    SECRET_KEY = os.environ["SECRET_KEY"]
    # Configuracion de mongodb
    MONGODB_SETTINGS = {
        "db": "ati",
        "host": "mongodb",
        "port": 27017
    }

    # Configuracion de flask
    TESTING = False

    # === Configuracion de FlaskUser ====
    USER_APP_NAME = "ATI Social"      # Shown in and email templates and page footers
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Se le indicca al usuario ingresar la contraseña de nuevo

    # - E-mail settings
    USER_ENABLE_EMAIL = True      # Enable email authentication
    USER_EMAIL_SENDER_EMAIL = "noresponder@ati.com"
    USER_EMAIL_SENDER_NAME = "ATI"
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = True
    USER_ENABLE_CONFIRM_EMAIL = False
    MAIL_SUPPRESS_SEND = False
    MAIL_PORT = 8025
    MAIL_SERVER = "email_server"

    # Override urls

    USER_REGISTER_URL = "/registro"
    USER_LOGIN_URL = "/"
    # USER_LOGOUT_URL = ""

    # Override templates

    USER_LOGIN_TEMPLATE = "usuario/login.html"
    #USER_RESET_PASSWORD_TEMPLATE = ""
    USER_REGISTER_TEMPLATE = "usuario/registro.html"

    USER_AFTER_LOGIN_ENDPOINT = "mural_blueprint.index"
    USER_AFTER_REGISTER_ENDPOINT = "mural_blueprint.index"
    USER_AFTER_LOGOUT_ENDPOINT = "user.login"

    # === Configuracion FlaskBabel ===
    BABEL_DEFAULT_LOCALE = "es_VE"

class TestingConfig(Config):
    """
    Configuracion para pruebas unitarias
    """
    TESTING = True
    SERVER_NAME = "localhost.localdomain:5000"
