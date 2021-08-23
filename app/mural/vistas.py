from flask import Blueprint, render_template, request, redirect, url_for
from flask_user.decorators import login_required
from flask_user import current_user
from app.mural.forms import ( PublicacionForm, ComentarioForm, SearchBarForm)
from app.models.mural import ( Publicacion, Comentario )
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

@mural_blueprint.route("/publicacion/detalle", methods=['GET', 'POST'])
def detalle_publicacion():

    user = current_user
    form = ComentarioForm(request.form)

    publicacionID = request.args.get('publicacionID')
    publicacion = Publicacion.objects.get(id=publicacionID)

    if request.method == 'POST' and form.validate():

        comentario = Comentario()
        comentario.contenido = form.contenido.data
        comentario.fecha = datetime.now()
        comentario.usuario = user
        comentario.publicacion = publicacion

        comentario.save()

        publicacion.comentarios.append(comentario)
        publicacion.save()

    return render_template("mural/muralDetallePublicacion.html",
                            detalleButton=False, 
                            publicacion=publicacion, 
                            form=form)

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
@mural_blueprint.route("/resultados-busqueda", methods=['GET', 'POST'])
def resultados_busqueda():

    form = SearchBarForm(request.form)

    tipo_busqueda = request.args.get('tipo_busqueda')
    texto_busqueda = request.args.get('texto_busqueda')

    filtered_users = User.objects(nombre__icontains = texto_busqueda)

    return render_template("mural/resultados_busqueda.html", form=form, filtered_users = filtered_users)
