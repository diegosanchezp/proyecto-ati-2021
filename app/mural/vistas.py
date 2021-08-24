from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash,
)
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.mural.forms import ( PublicacionForm, ComentarioForm, SearchBarForm)
from app.models.mural import ( Publicacion, Comentario )
from app.models.user import ( User )
from app.models.mural import TIPO_PUBLICACIONES
from app.utils import get_upload_path
from datetime import datetime
from werkzeug.utils import secure_filename

import math

mural_blueprint = Blueprint('mural_blueprint', __name__, template_folder='templates')

@mural_blueprint.route("/", methods=["GET"])
@login_required
def index_proxy():
    """
    Proxi view to redirect from login and register
    beacuse flask_user endpoint doesn't support parameters
    """
    return redirect(url_for("mural_blueprint.index", page=1))


@mural_blueprint.route("/<int:page>", methods=["GET"])
@login_required
def index(page: int):
    """ Vista principal del mural """
    form = SearchBarForm(request.form)
    ## Filtrar publicaciones ##
    ## Hay que mejorar un poco la logica ##

    publicaciones_publicas = Publicacion.objects(tipo_publicacion=TIPO_PUBLICACIONES[0][0]).order_by('-fecha')


    return render_template("mural/mural.html",
        # Cambiar per_page a un numero más razonable por ejemplo
        # per_page=10
       publicaciones=publicaciones_publicas.paginate(page=page, per_page=2),
       form=form,
       detalleButton=True
   )

@mural_blueprint.route("/publicacion/detalle/<string:publicacionID>", methods=['GET', 'POST'])
def detalle_publicacion(publicacionID: str):
    form = ComentarioForm(request.form)

    publicacion = Publicacion.objects.get(id=publicacionID)

    if request.method == 'POST' and form.validate():
        comentario = Comentario(
                contenido = form.contenido.data,
                fecha = datetime.now(),
                usuario = current_user,
                publicacion = publicacion
            )

        comentario.save()

        publicacion.comentarios.append(comentario)
        publicacion.save()

    return render_template("mural/muralDetallePublicacion.html",
                            detalleButton=False, 
                            publicacion=publicacion, 
                            form=form)

@mural_blueprint.route("/crear-publicacion", methods=['GET', 'POST'])
@login_required
def create_publication():
    """ Vista para crear publicaciones """
    from flask import current_app

    form = PublicacionForm(request.form)

    if request.method == 'POST' and form.validate():

        publicacion = Publicacion(
            contenido=form.contenido.data,
            tipo_publicacion=form.tipo_publicacion.data,
            fecha=datetime.now(),
            autor=current_user,
        )

        # Guardar para obtener un id
        publicacion.save()

        # Guardar imagenes

        foto_path = Publicacion.get_images_path()

        for file_to_upload in request.files.getlist(form.images.name):

            # Todo image name validation, before this step
            real_img_name = f"{publicacion.id}-{file_to_upload.filename}"
            file_path = foto_path / real_img_name
            file_to_upload.save(file_path)
            publicacion.imagenes.append((real_img_name))

        # Guardar los nombres de las imagenes
        publicacion.save()

        # Informar al usuario que se creo la publicacion

        flash(_("Publicación creada"), 'success')

        return redirect(url_for('mural_blueprint.index', page=1))

    return render_template("mural/create_publication.html", form=form)

""" Resultados busqueda """
@mural_blueprint.route("/resultados-busqueda", methods=['GET', 'POST'])
def resultados_busqueda():

    form = SearchBarForm(request.form)

    tipo_busqueda = request.args.get('tipo_busqueda')
    texto_busqueda = request.args.get('texto_busqueda')

    filtered_users = User.objects(nombre__icontains = texto_busqueda)

    return render_template("mural/resultados_busqueda.html", form=form, filtered_users = filtered_users)
