from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash,
)
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.usuario.forms import ConfigForm, PrivacyForm
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

@usuario_blueprint.route("/editar-privacidad", methods=['GET', 'POST'])
@login_required
def editar_privacidad():
    """
    Vista de editar privacidad
    """
    form = PrivacyForm(request.form, obj=current_user.config)
    if request.method == 'POST' and form.validate():
        updated_config = form.save()
        # Update form with data from the updated config object
        form = PrivacyForm(obj=updated_config)
    return render_template("usuario/editar_privacidad.html", form=form)

@usuario_blueprint.route("/configuracion", methods=['GET', 'POST'])
@login_required
def configuracion():
    """
    Vista de configuracion
    """
    # Obtener un formulario con la data proveniente del request y del
    # objeto config del usuario autenticado
    form = ConfigForm(formdata=request.form, obj=current_user.config)
    if request.method == 'POST' and form.validate():
        # Guardar la config
        updated_config = form.save()
        # Update form with data from the updated config object
        form = ConfigForm(obj=updated_config)

        flash(_("Config Guardada"), "success")

    return render_template("usuario/configuracion.html", form=form)

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
