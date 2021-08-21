from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash,
)
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.mural.forms import ( PublicacionForm, ComentarioForm, SearchBarForm)
from app.models.mural import ( Publicacion )
from app.models.user import ( User )
from datetime import datetime
import math

mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

""" Vista principal del mural """
@mural_blueprint.route("/")
@login_required
def index():

    form = SearchBarForm(request.form)
    publicaciones_publicas = []

    ## Filtrar publicaciones ##
    ## Hay que mejorar un poco la logica ##
    for publicacion in Publicacion.objects().order_by('-fecha'):
        if publicacion.tipo_publicacion == 'publica':
            publicaciones_publicas.append(publicacion)

    pagination_number = math.ceil(len(publicaciones_publicas)/10)

    return render_template("mural/mural.html", 
                           publicaciones=publicaciones_publicas,
                           pagination_number=pagination_number,
                           form=form,
                           detalleButton=True)

@mural_blueprint.route("/publicacion/detalle")
def publicaciones():
    return render_template("mural/muralDetallePublicacion.html", detalleButton=False)

@mural_blueprint.route("/crear-publicacion", methods=['GET', 'POST'])
@login_required
def create_publication():
    """ Vista para crear publicaciones """

    form = PublicacionForm(request.form)

    if request.method == 'POST' and form.validate():

        publicacion = Publicacion(
            contenido=form.contenido.data,
            tipo_publicacion=form.tipo_publicacion.data,
            fecha=datetime.now(),
            autor=current_user,
        )

        publicacion.save()

        # Informar al usuario que se creo la publicacion

        flash(_("Publicación creada"), 'success')

        return redirect(url_for('mural_blueprint.index'))

    return render_template("mural/create_publication.html", form=form)

""" Resultados busqueda """
@mural_blueprint.route("/resultados-busqueda", methods=['GET', 'POST'])
def resultados_busqueda():

    form = SearchBarForm(request.form)

    tipo_busqueda = request.args.get('tipo_busqueda')
    texto_busqueda = request.args.get('texto_busqueda')

    filtered_users = User.objects(nombre__icontains = texto_busqueda)

    return render_template("mural/resultados_busqueda.html", form=form, filtered_users = filtered_users)
