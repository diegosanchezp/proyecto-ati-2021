from flask import (
    Blueprint, render_template,
    request, flash, redirect
)
from app.models.user import USUARIO_GENEROS
from app.models.mural import ( Publicacion, TIPO_PUBLICACIONES ) 
from flask_login import current_user
from flask_babel import _
from flask_user.decorators import login_required

usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User
from app.models.peticion import (
    Peticion,
    TipoPeticiones,
    PeticionEstado,
    PeticionEvento,
    NotiEvento,
    Notificacion,
    TipoNotificaciones,
)

@usuario_blueprint.post("/procesar-peticion-amistad")
@login_required
def procesar_peticion_amistad():
    """
    Vista para aceptar o rechazar solicitudes de amistad

    La persona quien creo la solicitud de amistad es
    peticion.emisor

    La persona quien acepta la solicitud de amistad es el
    current_user
    """
    try:
        peticion = Peticion.objects.get(id=request.form["peticion_id"])
    except Peticion.DoesNotExist:
        flash(_("La peticion que intentas actualizar no existe"), "danger")
        return redirect(request.args.redirect)


    if not peticion.tipo == TipoPeticiones.AMISTAD:
        flash(_("Error: la peticion no es de tipo amistad"), "danger")
        return redirect(request.args.get("redirect"))

    # Peticion.receptor should be the current_user
    if not current_user == peticion.receptor:
        flash(_("Esta peticion no te corresponde"), "danger")
        return redirect(request.args.get("redirect"))

    n = Notificacion(
        tipo=TipoNotificaciones.SOLICITUD_AMISTAD,
        recurso=peticion,
        emisor=peticion.receptor,
        receptor=peticion.emisor,
    )

    if request.form["action"] == PeticionEvento.ACEPTAR.value:
        peticion.transition(PeticionEvento.ACEPTAR)
        flash(_("Solicitud aceptada"), 'success')
        n.descripcion = f"ha aceptado tu {peticion.tipo.value}"

        # Añadirse como amigos

        # La persona quien acepta la solicitud de amistad
        current_user.amigos.append(peticion.emisor)
        current_user.save()

        # La persona quien creo la solicitud de amistad
        peticion.emisor.amigos.append(current_user)
        peticion.emisor.save()
        
    if request.form["action"] == PeticionEvento.RECHAZAR.value:
        peticion.transition(PeticionEvento.RECHAZAR)
        flash(_("Solicitud rechazada"), 'warning')
        n.descripcion = f"ha rechazado tu {peticion.tipo.value}"

    # Marcar como leida la notificaion asociada a la peticion
    try:
        npeticion = Notificacion.objects.get(receptor=current_user,emisor=peticion.emisor,recurso=peticion)
        npeticion.transition(NotiEvento.LEER)
        npeticion.save()
    except Notificacion.DoesNotExist:
        pass

    n.save()
    peticion.save()

    return redirect(request.args.get("redirect"))

@usuario_blueprint.route("/ver-perfil/<username>", methods=["POST", "GET"])
@login_required
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

    # Solicitar amistad a un usuario
    if request.method == "POST" and request.form["action"] == "SOLICITAR_AMISTAD":
        if not it_is_the_current_user:
            
            solicitud = Peticion( estado = PeticionEstado.ESPERA,
                                  tipo = TipoPeticiones.AMISTAD,
                                  emisor = current_user,
                                  receptor = target_user
                                )
            solicitud.save()

            n = Notificacion(
                tipo=TipoNotificaciones.SOLICITUD_AMISTAD,
                emisor=current_user,
                receptor=target_user,
                descripcion=f"quiere ser tu amigo",
                recurso=solicitud,
            )

            n.save()

            flash(_("Solicitud amistad enviada"), 'success')
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
    if not it_is_the_current_user:
        # Soy la persona que realizo la solicitud
        peticion = Peticion.objects(emisor=current_user,receptor=target_user, estado=PeticionEstado.ESPERA).first()
        if not peticion:
            # Soy la persona que recibe la solicitud
            peticion = Peticion.objects(emisor=target_user,receptor=current_user, estado=PeticionEstado.ESPERA).first()
    return render_template("usuario/ver_perfil.html",
        target_user = target_user,
        it_is_the_current_user = it_is_the_current_user,
        is_friend=target_user in current_user.amigos,
        peticion=peticion,
        publicaciones = publicaciones,
        PeticionEvento=PeticionEvento,
        PeticionEstado=PeticionEstado,
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
