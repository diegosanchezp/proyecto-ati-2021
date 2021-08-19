from flask import Blueprint, render_template, request, redirect, url_for
from flask_user.decorators import login_required
from flask_user import current_user
from app.mural.forms import ( PublicacionForm, ComentarioForm )
from app.models.mural import ( Publicacion )
from datetime import datetime

mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

""" Vista principal del mural """
@mural_blueprint.route("/")
@login_required
def index():

    publicaciones_publicas = []

    ## Filtrar publicaciones ##
    ## Hay que mejorar un poco la logica ##
    for publicacion in Publicacion.objects:
        if publicacion.tipo_publicacion == 'publica':
            publicaciones_publicas.append(publicacion)

    return render_template("mural/mural.html", publicaciones=publicaciones_publicas ,detalleButton=True)

@mural_blueprint.route("/publicacion/detalle")
def publicaciones():
    return render_template("mural/muralDetallePublicacion.html", detalleButton=False)

""" Vista para crear publicaciones """
@mural_blueprint.route("/crear-publicacion", methods=['GET', 'POST'])
def create_publication():

    user = current_user
    form = PublicacionForm(request.form)

    if request.method == 'POST' and form.validate():

        publicacion = Publicacion()
        publicacion.contenido = form.contenido.data
        publicacion.tipo_publicacion = form.tipo_publicacion.data
        publicacion.fecha = datetime.now()
        publicacion.autor = user
        
        publicacion.save()

        return redirect(url_for('mural_blueprint.index'))

    return render_template("mural/create_publication.html", form=form)

""" Resultados busqueda """
@mural_blueprint.route("/resultados-busqueda")
def resultados_busqueda():
    return render_template("mural/resultados_busqueda.html")
