from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash,
)
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.usuario.forms import ( ConfigForm)
from app.models.user import ( UserConfig, UserNotificationsConfig)
import math

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')

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

@login_required
@usuario_blueprint.route("/editar-privacidad")
def editar_privacidad():
    """
    Vista de editar privacidad
    """
    form = ConfigForm(request.form)

    return render_template("usuario/editar_privacidad.html", form=form, UserConfig=UserConfig)

@login_required
@usuario_blueprint.route("/configuracion", methods=['GET', 'POST'])
def configuracion():
    """
    Vista de configuracion
    """
    form = ConfigForm(request.form)

    if request.method == 'POST':
        userConfig = UserConfig(
                color_perfil = request.form['colorProfile'],
                color_muro = request.form['colorWall']
            )

        userNotificationsConfig = UserNotificationsConfig(
                comentarios = request.form['emailMessage'],
                mensajes_chat = request.form['emailNotification'],
                amigos_conectados = request.form['emailFriend'],
            )

        userConfig.save()

    return render_template("usuario/configuracion.html", form=form, UserNotificationsConfig=UserNotificationsConfig, UserConfig=UserConfig)

    

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
