import flask
from flask_mongoengine import MongoEngine
from app.utils import (
    register_blueprints,
    before_request,
)
from flask_babel import Babel
from flask_login.mixins import AnonymousUserMixin

# Instanciar extensiones de flask
db = MongoEngine()
babel = Babel()

def create_app(config_class="Config"):
    """ Flask application factory """

    # Instanciar aplicacion de flask
    app = flask.Flask(__name__)
    # Cargar configuracion
    app.config.from_object(f"app.config.{config_class}")
    app.jinja_env.add_extension('jinja2.ext.do')
    # Setup Flask-MongoEngine
    db.init_app(app)

    # Verificar si la conexion a base de datos esta funcionando
    if not app.testing:
        try:
            MongoClient = db.get_connection()
            MongoClient.admin.command('ismaster')
        except Exception:
            raise Exception('=== No se puede conectar a base de datos, terminando programa ===')

    # Setup Flask-User and specify the User data-model
    from app.models.user import User
    from app.usuario.user_manager import CustomUserManager
    user_manager = CustomUserManager(app, db, User)

    # Initialize Flask-Babel
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        from flask_user import current_user
        # if a user is logged in, use the locale from the user settings
        if not isinstance(current_user, AnonymousUserMixin):
            return current_user.config.lenguaje
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.

    # Registar todos los blueprints
    register_blueprints(app)

    # Cargar funciones que se ejecutan antes de cada request
    before_request(app)

    return app
