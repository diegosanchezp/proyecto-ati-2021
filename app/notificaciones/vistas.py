from flask import (
    Blueprint,
    render_template,
    request,
    flash,
)
from flask_login import current_user
from app.models.peticion import (
    Notificacion, NotificacionEstado,
    NotiEvento,
    TipoNotificaciones
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

    notificaciones = Notificacion.objects.get_notificaciones_usuario()
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
            )
