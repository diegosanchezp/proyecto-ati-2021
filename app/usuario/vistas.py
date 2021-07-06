from flask import Blueprint, render_template
usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')

@usuario_blueprint.route("/")
def index():
    """
    Login, vista principal
    """
    return render_template("usuario/login.html")
