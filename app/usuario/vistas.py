from flask import (
    Blueprint,
    render_template,
    url_for
)

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')

from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

facebook_blueprint = make_facebook_blueprint(
    redirect_to="user.fb_callback",
    scope="email,user_birthday,user_gender,public_profile"
)

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

@usuario_blueprint.route("/ver-perfil")
def ver_perfil():
    """
    Vista de ver perfil
    """
    return render_template("usuario/ver_perfil.html")

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

@usuario_blueprint.route("/mis-amigos")
def mis_amigos():
    """
    Mis amigos
    """
    return render_template("usuario/mis_amigos.html")

@usuario_blueprint.route("/mi-perfil")
def mi_perfil():
    """
    Mi perfil
    """
    return render_template("usuario/mi_perfil.html")
