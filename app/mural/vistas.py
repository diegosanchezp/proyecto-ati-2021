from flask import Blueprint, render_template
mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

@mural_blueprint.route("/")
def index():
    """
    Vista principal del mural
    """
    return render_template("mural/mural.html")

@mural_blueprint.route("/publicaciones")
def publicaciones():
    return "Hola Publicaciones"

@mural_blueprint.route("/create_publication")
def create_publication():
    """
    Vista para crear publicaciones
    """
    return render_template("mural/create_publication.html")