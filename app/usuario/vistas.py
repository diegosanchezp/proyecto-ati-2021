from flask import (
    Blueprint, render_template,
    request, flash, redirect
)
from app.models.user import USUARIO_GENEROS
from app.models.mural import ( Publicacion, TIPO_PUBLICACIONES ) 
from flask_login import current_user
from flask_babel import _

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User, Solicitud_Amistad, ESTADO_SOLICITUD

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

    if it_is_the_current_user:
        publicaciones = Publicacion.objects(autor=current_user).order_by('-fecha')
    else:
        publicaciones = Publicacion.objects(autor=target_user).order_by('-fecha')

    # Chequear si hay una solicitud de amistad entre las personas
    is_solicitud = 'none'
    for solicitud in current_user.solicitudes:
        if solicitud.emisor == current_user:
            is_solicitud = 'emisor'
            break
        elif solicitud.receptor == current_user :
            is_solicitud = 'receptor'
            break
        else:
            is_solicitud = 'none'
            break


    if request.method == "POST" and request.form["action"] == "SOLICITAR_AMISTAD":
        # Solicitar amistad a un usuario
        if not it_is_the_current_user:
            solicitud = Solicitud_Amistad( estado = ESTADO_SOLICITUD[0][0],
                                           emisor = current_user,
                                           receptor = target_user,
                                         )
            solicitud.save()

            current_user.solicitudes.append(solicitud)
            current_user.save()

            target_user.solicitudes.append(solicitud)
            target_user.save()

        flash(_("Solicitud enviada"), 'success')
        return redirect(request.url)

    if request.method == "POST" and request.form["action"] == "ACEPTAR_SOLICITUD":
        # Aceptar amigo
        if not it_is_the_current_user:
            if is_solicitud == 'emisor':
                solicitud = Solicitud_Amistad.objects.get_or_404(emisor=current_user)
            if is_solicitud == 'receptor':
                solicitud = Solicitud_Amistad.objects.get_or_404(receptor=current_user)

            # Update current user
            current_user.solicitudes.remove(solicitud)
            current_user.amigos.append(target_user)
            current_user.save()

            target_user.solicitudes.remove(solicitud)
            target_user.amigos.append(current_user)
            target_user.save()

            solicitud.delete()

            flash(_("Amistad aceptada"), 'success')
            return redirect(request.url)

    if request.method == "POST" and request.form["action"] == "RECHAZAR_SOLICITUD":
        # Aceptar amigo
        if not it_is_the_current_user:
            if is_solicitud == 'emisor':
                solicitud = Solicitud_Amistad.objects.get_or_404(emisor=current_user)
            if is_solicitud == 'receptor':
                solicitud = Solicitud_Amistad.objects.get_or_404(receptor=current_user)

            # Update current user
            current_user.solicitudes.remove(solicitud)
            current_user.save()

            target_user.solicitudes.remove(solicitud)
            target_user.save()

            solicitud.delete()

            flash(_("Amistad rechazada"), 'success')
            return redirect(request.url)

    if request.method == "POST" and request.form["action"] == "BORRAR_AMIGO":
        # Borrar amigo
        if not it_is_the_current_user:
            current_user.amigos.remove(target_user)
            current_user.save()

            target_user.amigos.remove(current_user)
            target_user.save()

            flash(_("Amistad borrada"), 'success')
            return redirect(request.url)

    return render_template("usuario/ver_perfil.html",
        target_user = target_user,
        it_is_the_current_user = it_is_the_current_user,
        is_friend=target_user in current_user.amigos,
        is_solicitud = is_solicitud,
        publicaciones = publicaciones,
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
