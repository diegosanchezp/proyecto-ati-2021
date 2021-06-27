"""
Archivo de configuración de flask
"""

class Config:
    """
    Clase de principal configuracion de flask
    """

    # Configuracion de mongodb
    MONGODB_SETTINGS = {
        "db": "ati",
        "host": "mongodb",
        "port": 27017
    }

    # Configuracion de flask
    TESTING = False

class TestingConfig(Config):
    """
    Configuracion para pruebas unitarias
    """
    TESTING = True
