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

    # Facebook OAUTH login
    FACEBOOK_OAUTH_CLIENT_ID = "138076435140848"
    FACEBOOK_OAUTH_CLIENT_SECRET = "44b507b0fb348cf0b380ddb7f5cfa20c"

    # === Configuracion para archivos de usuario ===

    MAX_CONTENT_LENGTH = 1024*768
    UPLOAD_FOLDER = "uploads"
    PUBLICACIONES_FOLDER = "publicaciones"

    # === Configuracion de FlaskUser ====
    USER_ENABLE_AUTH0 = True
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
    # - Override urls

    USER_REGISTER_URL = "/registro"
    USER_LOGIN_URL = "/"
    USER_FORGOT_PASSWORD_URL = "/recuperar"
    USER_CHANGE_PASSWORD_URL = "/editar-password"

    # USER_LOGOUT_URL = ""
    USER_EDIT_USER_PROFILE_URL = "/editar-perfil"

    # - Override templates

    USER_LOGIN_TEMPLATE = "usuario/login.html"
    USER_LOGIN_AUTH0_TEMPLATE = "usuario/login.html"
    USER_FORGOT_PASSWORD_TEMPLATE = "usuario/recuperar_password.html"
    USER_REGISTER_TEMPLATE = "usuario/registro.html"
    USER_CHANGE_PASSWORD_TEMPLATE = "usuario/editar_password.html"
    USER_EDIT_USER_PROFILE_TEMPLATE = "usuario/editar_perfil.html"

    USER_RESET_PASSWORD_TEMPLATE = "usuario/reset_password.html"

    USER_EDIT_USER_PROFILE_TEMPLATE = "usuario/editar_perfil.html" 

    USER_AFTER_LOGIN_ENDPOINT = "mural_blueprint.index_proxy"
    USER_AFTER_LOGOUT_ENDPOINT = "user.login"
    USER_AFTER_REGISTER_ENDPOINT = "mural_blueprint.index_proxy"
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = "usuario_blueprint.recuperar_token"
    USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = "user.edit_user_profile"
    USER_AFTER_LOGOUT_ENDPOINT = "user.login"

    # === Configuracion FlaskBabel ===
    BABEL_DEFAULT_LOCALE = "es_VE"

class TestingConfig(Config):
    """
    Configuracion para pruebas unitarias
    """
    TESTING = True
    SERVER_NAME = "localhost.localdomain:5000"
