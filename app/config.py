"""
Archivo de configuración de flask
"""
import os

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

    # Configuracion de FlaskUser
    USER_APP_NAME = "ATI Social"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True      # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Se le indicca al usuario ingresar la contraseña de nuevo
    USER_EMAIL_SENDER_EMAIL = "noresponder@ati.com"
    USER_EMAIL_SENDER_NAME = "ATI"

class TestingConfig(Config):
    """
    Configuracion para pruebas unitarias
    """
    TESTING = True
