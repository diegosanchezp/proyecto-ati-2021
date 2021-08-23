from flask import (
    Blueprint, send_file, abort, send_from_directory,
)
from app.models.user import User
from app.models.mural import Publicacion
from app.utils import get_upload_path

media_blueprint = Blueprint('media_blueprint', __name__)

@media_blueprint.route("foto_perfil/<string:user_id>", methods=["GET"])
def foto_perfil(user_id):
    """
    Obtener la foto de perfil de un usuario
    """
    # Obtener usuario
    user = User.objects.get(id=user_id)
    if bool(user.foto):

        # Retornar
        return send_file(
            path_or_file=user.foto,
            mimetype=user.foto.content_type
        )

    # Set appropiate
    return abort(404)

@media_blueprint.route("publicacion/<string:file_name>", methods=["GET"])
def foto_publicacion(file_name):
    """
    Obtener la foto de una publicacion
    """
    from flask import current_app

    foto_path = get_upload_path(current_app) / current_app.config["PUBLICACIONES_FOLDER"]
    return send_from_directory(foto_path,file_name)
