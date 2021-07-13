from flask import Blueprint, render_template
mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

@mural_blueprint.route("/")
def index():
    """
    Vista principal del mural
    """
    return render_template("mural/mural.html", detalleButton=True)

@mural_blueprint.route("/publicacion/detalle")
def publicaciones():
    return render_template("mural/muralDetallePublicacion.html", detalleButton=False)
