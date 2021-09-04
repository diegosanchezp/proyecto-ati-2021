"""
Modelos relacionados con usuarios
"""
from flask import url_for
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_user import UserMixin
from app import db
from app.constants import MAX_IMAGE_SIZE
from typing import Union, List

class UserNotificationsConfig(db.EmbeddedDocument):
    """
    Configuracion personal de las notificaciones

    Todas estas notificaciones le llegaran al usuario y las podrá
    ver en la vista de notificaciones
    """
    comentarios = db.BooleanField(default=True)
    mensajes_chat = db.BooleanField(default=True)
    amigos_conectados = db.BooleanField(default=True)

    def __str__(self):
        return f"comentarios={self.comentarios} mensajes_chat={self.mensajes_chat}"

class UserConfig(db.Document):
    """
    Configuracion de un usuario
    """
    color_perfil = db.StringField()
    color_muro = db.StringField()
    publicaciones_privadas = db.BooleanField(default=False)
    notificaciones = db.EmbeddedDocumentField("UserNotificationsConfig")

USUARIO_GENEROS = (
    ("M", _l("Masculino")),
    ("F", _l("Femenino")),
)


class User(db.Document, UserMixin):
    """
    Modelo usuario
    """

    # User authentication information
    username = db.StringField(unique=True)
    password = db.StringField()
    active = db.BooleanField(db_field="is_active", default=True)
    email = db.EmailField()
    email_confirmed_at = db.DateTimeField(default=None)

    # Fields pedido en los requerimientos
    nombre = db.StringField()
    foto = db.ImageField(size=MAX_IMAGE_SIZE) # foto se guarda en la db
    ci = db.IntField(unique=True)
    fecha_nacimiento = db.DateTimeField()
    genero = db.StringField(choices=USUARIO_GENEROS)
    descripcion = db.StringField()
    color = db.StringField()
    libro = db.StringField()
    musica = db.StringField()
    video_juegos = db.ListField(db.StringField())
    lenguajes_programacion = db.ListField(db.StringField())

    # Relaciones
    config = db.ReferenceField("UserConfig")
    amigos = db.ListField(db.ReferenceField("self"))
    meta = {
        "cascade": True,
    }

    def __init__(self, *args, **kwargs):
        """
        Extending this method to put some default field values
        """

        super().__init__(*args, **kwargs)

        self.set_username_from_nombre()

        # Create default configuration
        if self.config is None:
            self.config = UserConfig(notificaciones=UserNotificationsConfig())

    def set_username_from_nombre(self):
        """ Create username from nombre """
        if self.username is None and self.nombre is not None:
            self.username = self.nombre.lower().replace(" ", "_")

    def get_foto_url(self) -> Union[str, None]:
        if bool(self.foto):
            return url_for("media_blueprint.foto_perfil", user_id=self.id)
        else:
            return None

    def get_genero_string(self) -> str:
        """
        Obtener un string para el genero
        """
        return USUARIO_GENEROS[1][1] if self.genero=='F' else USUARIO_GENEROS[0][1]

    def save(self, *args, **kwargs):

        self.config.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"username={self.username} nombre={self.nombre} ci={self.ci}"
