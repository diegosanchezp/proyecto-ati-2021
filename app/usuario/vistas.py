from flask import (
    Blueprint, render_template,
    request, flash, url_for,
    redirect,
)
from flask_login import current_user
from flask_user.decorators import login_required
from flask_user import current_user
from flask_babel import _
from app.usuario.forms import ConfigForm, PrivacyForm
from app.models.user import (
    UserConfig, UserNotificationsConfig, USUARIO_GENEROS
)

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User

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
        flash(_("Config privacidad guardada"), "success")
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
        return redirect("configuracion")

    return render_template("usuario/configuracion.html", form=form)

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
