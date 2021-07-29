"""
Modelos relacionados con usuarios
"""
from flask_babel import lazy_gettext as _l
from flask_user import UserMixin
from app import db
from app.constants import MAX_IMAGE_SIZE


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

    # Fields pedido en los requerimientos
    nombre = db.StringField()
    foto = db.ImageField(size=MAX_IMAGE_SIZE) # foto se guarda en la db
    email = db.EmailField()
    ci = db.IntField(unique=True)
    fecha_nacimiento = db.DateTimeField()
    genero = db.StringField(choices=USUARIO_GENEROS)
    descripcion = db.StringField()
    color = db.StringField()
    libro = db.StringField()
    musica = db.StringField()
    video_juegos = db.ListField()
    lenguajes_programacion = db.ListField()
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

        # Create username from nombre
        if self.username is None and self.nombre is not None:
            self.username = self.nombre.lower().replace(" ", "_")

        # Create default configuration
        if self.config is None:
            self.config = UserConfig(notificaciones=UserNotificationsConfig())

    def save(self, *args, **kwargs):
        self.config.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"username={self.username} nombre={self.nombre} ci={self.ci}"
