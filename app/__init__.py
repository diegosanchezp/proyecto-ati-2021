import flask
from flask_user import UserManager
from flask_mongoengine import MongoEngine
from app.utils import register_blueprints
from flask_babel import Babel

# Instanciar extensiones de flask
db = MongoEngine()
babel = Babel()
def create_app():
    """ Flask application factory """

    # Instanciar aplicacion de flask
    app = flask.Flask(__name__)
    # Cargar configuracion
    app.config.from_object("app.config.Config")

    # Setup Flask-MongoEngine
    db.init_app(app)

    # Verificar si la conexion a base de datos esta funcionando
    try:
        MongoClient = db.get_connection()
        MongoClient.admin.command('ismaster')
    except Exception:
        raise Exception('=== No se puede conectar a base de datos, terminando programa ===')

    # Setup Flask-User and specify the User data-model
    from app.models.user import User
    user_manager = UserManager(app, db, User)

    # Initialize Flask-Babel
    babel.init_app(app)

    # Use the browser's language preferences to select an available translation
    @babel.localeselector
    def get_locale():
        from flask import request
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Registar todos los blueprints
    register_blueprints(app)
    return app
