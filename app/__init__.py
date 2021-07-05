import flask
from flask_user import UserManager
from flask_mongoengine import MongoEngine
from app.utils import register_blueprints

# Instanciar extensiones de flask
db = MongoEngine()
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

    # Registar todos los blueprints
    register_blueprints(app)
    return app
