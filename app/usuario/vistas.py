from flask import (
    Blueprint, render_template,
    request, flash,
)
from app.models.user import USUARIO_GENEROS
from flask_login import current_user
from flask_babel import _

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User

@usuario_blueprint.route("/recuperar")
def recuperar_password():
    """
    Vista de recuperación de contraseña
    """

    return render_template("usuario/recuperar_password.html")

@usuario_blueprint.route("/recuperar-token")
def recuperar_token():
    """
    Vista de recuperación de contraseña
    """

    return render_template("usuario/recuperar_pass_token_enviado.html")

@usuario_blueprint.route("/ver-perfil/<username>", methods=["POST", "GET"])
def ver_perfil(username):
    """
    Vista de ver perfil
    """
    target_user = User.objects.get_or_404(username=username)

    it_is_the_current_user = target_user == current_user

    if request.method == "POST" and request.form["action"] == "BORRAR AMIGO":
        # Delete a friend
        if not it_is_the_current_user:
            flash(_("Amistad borrada"), 'success')
            current_user.amigos.remove(target_user)
            current_user.save()

    return render_template("usuario/ver_perfil.html",
        target_user = target_user,
        it_is_the_current_user = it_is_the_current_user,
        is_friend=target_user in current_user.amigos
    )

@usuario_blueprint.route("/editar-privacidad")
def editar_privacidad():
    """
    Vista de editar privacidad
    """

    return render_template("usuario/editar_privacidad.html")

@usuario_blueprint.route("/configuracion")
def configuracion():
    """
    Vista de configuracion
    """

    return render_template("usuario/configuracion.html")

@usuario_blueprint.route("/amigos/<username>")
def amigos(username):
    target_user = User.objects.get_or_404(username=username)
    """
    Mis amigos
    """
    return render_template("usuario/amigos.html", target_user=target_user)

@usuario_blueprint.route("/mi-perfil")
def mi_perfil():
    """
    Mi perfil
    """
    return render_template("usuario/mi_perfil.html")
