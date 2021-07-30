from flask import Blueprint, render_template
from flask_user.decorators import login_required
mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

@mural_blueprint.route("/")
@login_required
def index():
    """
    Vista principal del mural
    """
    return render_template("mural/mural.html", detalleButton=True)

@mural_blueprint.route("/publicacion/detalle")
def publicaciones():
    return render_template("mural/muralDetallePublicacion.html", detalleButton=False)

@mural_blueprint.route("/crear-publicacion")
def create_publication():
    """
    Vista para crear publicaciones
    """
    return render_template("mural/create_publication.html")

@mural_blueprint.route("/resultados-busqueda")
def resultados_busqueda():
    """
    Resultados busqueda
    """
    return render_template("mural/resultados_busqueda.html")
