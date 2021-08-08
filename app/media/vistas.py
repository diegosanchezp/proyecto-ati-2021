from flask import Blueprint, send_file, abort
from app.models.user import User
import mimetypes

media_blueprint = Blueprint('media_blueprint', __name__)

@media_blueprint.route("foto_perfil/<string:user_id>", methods=["GET"])
def foto_perfil(user_id):
    """
    Obtener la foto de perfil de un usuario
    """
    # Obtener usuario
    user = User.objects.get(id=user_id)
    if bool(user.foto):
        mimetypes.init()
        # Obtener mimetype
        #mimetype=mimetypes.types_map.get(f"{user.foto.format.lower()}")
        
        # Retornar
        return send_file(
            path_or_file=user.foto,
            mimetype=user.foto.content_type
        )

    # Set appropiate
    return abort(404)
