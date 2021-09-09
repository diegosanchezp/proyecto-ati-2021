from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
)
from flask_login import current_user
from app.models.peticion import (
    Notificacion, NotificacionEstado,
    NotiEvento,
    TipoNotificaciones,
    TipoPeticiones,
    PeticionEvento,
    PeticionEstado,
    Peticion,
)
from flask_babel import _
from mongoengine.queryset.visitor import Q
from mongoengine import errors
from flask_user.decorators import login_required

notificaciones_blueprint = Blueprint('notificaciones_blueprint', __name__, template_folder='templates')

@notificaciones_blueprint.route("/<int:page>", methods=["POST", "GET"])
@login_required
def index(page: int):
    """
    Vista principal de las notificaciones
    """

    notificaciones = Notificacion.objects.get_notificaciones_usuario(current_user)
    if request.method == "POST" and request.form["action_event"] == NotiEvento.LEER.value:
        # Si la notificación pertenece al usuario y no esta leida
        try:
            # Actualizar estado a leida
            n = notificaciones.get(id=request.form["id_notificacion"])
            n.transition(NotiEvento.LEER)
            n.save()
            flash(_("Notificación leída"), 'success')
        except (Notificacion.DoesNotExist, errors.ValidationError) :
            flash(_("No se puede leer notificación no existente"), 'danger')


    return render_template(
            "notificaciones/notificaciones.html",
            notificaciones=notificaciones.paginate(page=page, per_page=10),
            TipoNotificaciones=TipoNotificaciones,
            NotiEvento=NotiEvento,
            PeticionEvento=PeticionEvento,
            PeticionEstado=PeticionEstado,
            )


@notificaciones_blueprint.post("/procesar-peticion-amistad")
@login_required
def procesar_peticion_amistad():
    """
    Vista para aceptar o rechazar solicitudes de amistad

    La persona quien creo la solicitud de amistad es
    peticion.emisor

    La persona quien acepta la solicitud de amistad es el
    current_user
    """
    # Retornar redireccion
    retdir = redirect(request.args.get("redirect"))

    try:
        peticion = Peticion.objects.get(id=request.form["peticion_id"])
    except Peticion.DoesNotExist:
        flash(_("La peticion que intentas actualizar no existe"), "danger")
        return retdir

    # Econtrar notificacion asociada a la peticion
    try:
        npeticion = Notificacion.objects.get(receptor=current_user,emisor=peticion.emisor,recurso=peticion)
    except Notificacion.DoesNotExist:
        return retdir

    if not peticion.tipo == TipoPeticiones.AMISTAD:
        flash(_("Error: la peticion no es de tipo amistad"), "danger")
        return retdir

    # Peticion.receptor should be the current_user
    if not current_user == peticion.receptor:
        flash(_("Esta peticion no te corresponde"), "danger")
        return retdir

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

        # -- Añadirse como amigos

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
    npeticion.transition(NotiEvento.LEER)
    npeticion.save()

    n.save()
    peticion.save()

    return redirect(request.args.get("redirect"))
