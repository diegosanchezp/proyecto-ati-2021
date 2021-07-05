from flask import Blueprint, render_template
notificaciones_blueprint = Blueprint('notificaciones_blueprint', __name__, template_folder='templates')

@notificaciones_blueprint.route("/")
def index():
    """
    Vista principal de las notificaciones
    """
    return render_template("notificaciones/notificaciones.html")
