from flask import Blueprint, send_file, abort
from app.models.user import User

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
