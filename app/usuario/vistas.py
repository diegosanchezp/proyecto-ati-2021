from flask import Blueprint, render_template
usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')

@usuario_blueprint.route("/")
def index():
    """
    Vista principal del chat
    """
    return render_template("usuario/usuario.html")
