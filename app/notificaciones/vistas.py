from flask import (
    Blueprint,
    render_template,
)
from flask_login import current_user
from app.models.peticion import (
    Notificacion, NotificacionEstado,
    TipoNotificaciones
)
from mongoengine.queryset.visitor import Q
from flask_user.decorators import login_required

notificaciones_blueprint = Blueprint('notificaciones_blueprint', __name__, template_folder='templates')



@notificaciones_blueprint.get("/<int:page>")
@login_required
def index(page: int):
    """
    Vista principal de las notificaciones
    """
    notificaciones = Notificacion.objects.get_notificaciones_usuario().paginate(page=page, per_page=2)

    return render_template("notificaciones/notificaciones.html", notificaciones=notificaciones, TipoNotificaciones=TipoNotificaciones)
