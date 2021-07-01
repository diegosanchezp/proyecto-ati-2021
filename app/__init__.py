import flask
from flask_user import UserManager
from flask_mongoengine import MongoEngine

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

    # Blueprints
    from app.mural.vistas import mural_blueprint
    from app.chat.chat import chat_blueprint

    # Registar blueprints
    app.register_blueprint(mural_blueprint, url_prefix="/mural")
    app.register_blueprint(chat_blueprint, url_prefix="/chat")
    return app
