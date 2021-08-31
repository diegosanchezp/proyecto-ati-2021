from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash,
)
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.mural.forms import (
    PublicacionForm,
    ComentarioForm,
    SearchBarForm
)
from app.models.mural import (
    Publicacion, Comentario,
    TIPO_PUBLICACIONES
)

from app.models.user import ( User )
from app.models.peticion import (
    Notificacion, TipoNotificaciones,
)
from app.utils import get_upload_path, allowed_file_extension
from datetime import datetime
from werkzeug.utils import secure_filename

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
       publicaciones=publicaciones_publicas.paginate(page=page, per_page=10),
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

        n = Notificacion(
            emisor=current_user,
            receptor=publicacion.autor,
            descripcion=f"{current_user.nombre} ha comentado tu publicación",
            tipo=TipoNotificaciones.COMENTARIO,
            recurso=publicacion,
        )
        n.save()
    return render_template("mural/muralDetallePublicacion.html",
                            detalleButton=False, 
                            publicacion=publicacion,
                            current_user=current_user,
                            form=form)

@mural_blueprint.route("/comentar_comentario/<string:comentarioID>", methods=['POST'])
def comentar_comentario(comentarioID: str):
    form = ComentarioForm(request.form)
    # Todo validar si el comentario respuesta pertence a la publicacion que se esta conectando
    comentario = Comentario.objects.get(id=comentarioID)
    
    if request.method == 'POST' and form.validate():
        comentario_respuesta = Comentario(
                contenido = form.contenido.data,
                fecha = datetime.now(),
                usuario = current_user,
                publicacion = comentario.publicacion
                )

        comentario_respuesta.save()

        comentario.respuestas.append(comentario_respuesta)
        comentario.save()

        # Enviar notificacion al autor del comentario que se esta
        # respondiendo
        n = Notificacion(
            emisor=current_user,
            receptor=comentario.usuario,
            descripcion=f"{current_user.nombre} ha respondido tu comentario de la publicacion",
            tipo=TipoNotificaciones.COMENTARIO,
            recurso=comentario.publicacion,
        )
        n.save()

        # Enviar notificacion al autor de la publicacion, de que su publicacion ha sido comentada
        n2 = Notificacion(
            emisor=current_user,
            receptor=comentario.publicacion.autor,
            descripcion=f"{current_user.nombre} ha comentado tu publicación",
            tipo=TipoNotificaciones.COMENTARIO,
            recurso=comentario.publicacion,
        )

        n2.save()

    return redirect(url_for('mural_blueprint.detalle_publicacion', publicacionID=comentario.publicacion.id))

@mural_blueprint.route("/crear-publicacion", methods=['GET', 'POST'])
@login_required
def create_publication():
    """ Vista para crear publicaciones """
    from flask import current_app
    template = "mural/create_publication.html"

    form = PublicacionForm(request.form)

    if request.method == 'POST' and form.validate():

        images_valid = []

        # Verificar que todas las imagenes sean validas, antes de guardar la publicacion
        for file_to_upload in request.files.getlist(form.images.name):
            # Sanitize filename
            filename = secure_filename(file_to_upload.filename)
            images_valid.append(allowed_file_extension(filename))

        if not all(images_valid):
            flash(_("Alguna de las imágenes son inválidas, intenta de nuevo"), "danger")
            return render_template(template, form=form)

        publicacion = Publicacion(
            contenido=form.contenido.data,
            tipo_publicacion=form.tipo_publicacion.data,
            fecha=datetime.now(),
            autor=current_user,
        )

        # Guardar para obtener un id
        publicacion.save()

        if form.images.data:
            foto_path = Publicacion.get_images_path()

            for file_to_upload in request.files.getlist(form.images.name):

                # Sanitize filename
                filename = secure_filename(file_to_upload.filename)

                if allowed_file_extension(filename):
                    real_img_name = f"{publicacion.id}-{filename}"
                    file_path = foto_path / real_img_name
                    file_to_upload.save(file_path)
                    publicacion.imagenes.append((real_img_name))

        # Guardar los nombres de las imagenes
        publicacion.save()

        # Informar al usuario que se creo la publicacion
        flash(_("Publicación creada"), 'success')

        return redirect(url_for('mural_blueprint.index', page=1))

    return render_template(template, form=form)

""" Resultados busqueda """
@mural_blueprint.route("/resultados-busqueda", methods=['GET', 'POST'])
def resultados_busqueda():

    form = SearchBarForm(request.form)

    tipo_busqueda = request.args.get('tipo_busqueda')
    texto_busqueda = request.args.get('texto_busqueda')

    filtered_users = User.objects(nombre__icontains = texto_busqueda)

    return render_template("mural/resultados_busqueda.html", form=form, filtered_users = filtered_users)
