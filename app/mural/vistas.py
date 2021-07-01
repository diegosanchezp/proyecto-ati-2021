from flask import Blueprint, render_template
mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')


from app import db

@mural_blueprint.route("/")
def index():
    """
    Vista principal del mural
    """
    return render_template("mural/mural.html")

@mural_blueprint.route("/publicaciones")
def publicaciones():
    return "Hola Publicaciones"
