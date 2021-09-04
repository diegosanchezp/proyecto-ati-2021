from flask import (
    Blueprint, render_template,
    request, flash, redirect
)
from app.models.user import USUARIO_GENEROS
from app.models.mural import ( Publicacion, TIPO_PUBLICACIONES ) 
from flask_login import current_user
from flask_babel import _

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User
from app.models.peticion import Peticion, TipoPeticiones, PeticionEstado

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
    peticiones_query = Peticion.objects()

    if peticiones_query:
        # Chequear si soy emisor de una solicitud
        try:
            emisor_query = peticiones_query.get(emisor=current_user, receptor=target_user)
            if emisor_query:
                is_solicitud = 'emisor'
        except Exception as e:
            print('\n\n\n\n')
            print('No se encontro current user EMISOR')
            print(e)
            print('\n\n\n\n')

        # Chequear si soy receptor de una solicitud
        try:
            receptor_query = peticiones_query.get(emisor=target_user, receptor=current_user)
            if receptor_query:
                is_solicitud = 'receptor'
        except Exception as e:
            print('\n\n\n\n')
            print('No se encontro current user RECEPTOR')
            print(e)
            print('\n\n\n\n')
        

    # Solicitar amistad a un usuario
    if request.method == "POST" and request.form["action"] == "SOLICITAR_AMISTAD":
        if not it_is_the_current_user:
            
            solicitud = Peticion( estado = PeticionEstado.ESPERA,
                                  tipo = TipoPeticiones.AMISTAD,
                                  emisor = current_user,
                                  receptor = target_user
                                )
            solicitud.save()

            flash(_("Solicitud enviada"), 'success')
            print('\n\n Solicitar')
            return redirect(request.url)

    # Aceptar amigo
    if request.method == "POST" and request.form["action"] == "ACEPTAR_SOLICITUD":
        if not it_is_the_current_user:

            # Update current user
            current_user.amigos.append(target_user)
            current_user.save()

            # Update target user
            target_user.amigos.append(current_user)
            target_user.save()

            # Aqui se debe de crear la notificacion

            # Una peticion aceptada es useless ya que is_friend se esta
            # chequeando directamente con la lista de amigos
            peticion_delete = Peticion.objects.get(emisor=target_user)
            peticion_delete.delete()

            flash(_("Solicitud aceptada"), 'success')
            print('\n\nAceptar solicitud')
            return redirect(request.url)

    # Rechazar amigo
    if request.method == "POST" and request.form["action"] == "RECHAZAR_SOLICITUD":
        if not it_is_the_current_user:

            # Aqui se debe de crear la notificacion

            # Una peticion rechazada no tiene mas logica de momento
            # Normalmente al ser rechazada se puede volver a solicitar amistad
            peticion_delete = Peticion.objects.get(emisor=target_user)
            peticion_delete.delete()

            flash(_("Solicitud Rechazada"), 'warning')
            print('\n\nRechazo')
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
