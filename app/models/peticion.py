from app import db
from enum import Enum
from flask_mongoengine import BaseQuerySet as QuerySet
from typing import Dict
from flask import g, url_for
from flask_babel import _
from mongoengine.queryset.visitor import Q
from app.models.user import User
class AbstractModel(db.Document):
    """
    Clase abstracta para modelos que utilizan maquinas de
    estado finito, requiere de las propiedades self.estado
    y self.maquina_estado
    """

    meta = {
        'abstract': True,
    }

    descripcion = db.StringField()
    emisor = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    receptor = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    def __str__(self):
        return f"estado={self.estado}"

    def transition(self, event) -> None:
        """
        Set the next state, given an event
        """
        try:
            next_state = self.maquina_estado[self.estado][event]
        except KeyError:
            raise Exception(
                f"Error: transicion no definida para estado: {self.estado} con event: {event}"
            ) from KeyError

        self.estado = next_state

class PeticionEstado(Enum):
    """
    Posibles estados de una petición
    """
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"
    ESPERA = "en espera"

class TipoPeticiones(Enum):
    CHAT = "peticion para chatear"
    AMISTAD = "solicitud de amistad"

class PeticionEvento(Enum):
    ACEPTAR = "aceptar"
    RECHAZAR = "rechazar"

class Peticion(AbstractModel):
    """
    Modelo de peticion
    """
    estado = db.EnumField(
        PeticionEstado,
        default=PeticionEstado.ESPERA
    )

    maquina_estado = {
        PeticionEstado.ESPERA: {
            PeticionEvento.ACEPTAR: PeticionEstado.ACEPTADA,
            PeticionEvento.RECHAZAR: PeticionEstado.RECHAZADA,
        }
    }

    tipo = db.EnumField(TipoPeticiones, required=True)

    def __str__(self):
        return f"emisor={self.emisor.username} receptor={self.receptor.username} estado={self.estado}"
#TIPO_NOTIFICACIONES = (
#    ("MENSAJE_CHAT", "mensaje chat"),
#    ("COMENTARIO", "comentario"),
#    ("AMIGO_CONECTADO", "amigo conectado"),
#)

class NotificacionEstado(Enum):
    """
    Estados de notificaciones
    """
    LEIDA = "leida"
    NO_LEIDA = "no leida"

class TipoNotificaciones(Enum):
    """
    Posibles tipo de notificaciones
    """
    MENSAJE_CHAT="mensaje chat"
    COMENTARIO = "comentario"
    AMIGO_CONECTADO = "amigo conectado"
    SOLICITUD_AMISTAD = "solicitud amistad"

class NotiEvento(Enum):
    LEER = "leer"

class NotiQuerySet(QuerySet):
    def get_notificaciones_usuario(self, user) -> QuerySet:
        """
        Obtener notificaciones del usuario autenticado
        """
        return self.filter(
            Q(receptor=user) & Q(estado=NotificacionEstado.NO_LEIDA)
        ).order_by("-id")

class Notificacion(AbstractModel):
    """
    Modelo de notificaciones
    """
    meta = {'queryset_class': NotiQuerySet}

    estado = db.EnumField(
        NotificacionEstado,
        default=NotificacionEstado.NO_LEIDA
    )

    maquina_estado = {
        NotificacionEstado.NO_LEIDA: {
            NotiEvento.LEER: NotificacionEstado.LEIDA
        }
    }

    tipo = db.EnumField(TipoNotificaciones, required=True)

    # Referencia al modelo (recurso) que genero la notificacion
    # - Comentario en una publicacion 
    # - Amigo conectado
    # - Mensaje de chat
    # - solicitud amistad

    # La Notificacion se borra si el recurso es borrado
    recurso = db.GenericReferenceField()
