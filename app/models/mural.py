from app import db
from app.constants import MAX_IMAGE_SIZE
from app.utils import get_upload_path
from flask_babel import _
from typing import List
from pathlib import Path # Utilizado como tipo
from flask import url_for
TIPO_PUBLICACIONES = [
    ("PUBLICA", _("Publica")),
    ("PRIVADA", _("Privada")),
]
from app.models.peticion import Notificacion

class Publicacion(db.Document):
    contenido = db.StringField()
    tipo_publicacion = db.StringField(choices=TIPO_PUBLICACIONES)
    fecha = db.DateTimeField()
    multimedia = db.FileField()
    # Arreglo de nombre de imagenes
    imagenes = db.ListField(db.StringField())
    # Videos sera por los momentos una lista de urls
    videos = db.ListField(db.URLField())

    enlaces = db.ListField(db.URLField())

    comentarios = db.ListField(db.ReferenceField("Comentario"))

    # La Publicacion se borra si el usuario autor se borra
    autor = db.ReferenceField("User", reverse_delete_rule=db.CASCADE)

    def __str__(self) -> str:
        return f"autor={self.autor} contenido={self.contenido}"

    def get_image_urls(self) -> List[str]:
        """
        Obtener urls para las imagenes de esta publicacion
        """
        return [url_for("media_blueprint.foto_publicacion", file_name=img_name) for img_name in self.imagenes]

    @staticmethod
    def get_images_path() -> Path:
        """
        Obtener el path de la carpeta en donde se guardan las
        imagenes de las publicaciones.
        """

        from flask import current_app as app
        return get_upload_path(app) / app.config["PUBLICACIONES_FOLDER"]

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        """
        - Borrar images cuando la publicacion se borre
        - Borrar notificaciones asociadas a la publicacion
        """
        imgs_path = cls.get_images_path()

        # - Borrar images cuando la publicacion se borre
        for img_name in document.imagenes:
            file_path = imgs_path / img_name
            file_path.unlink(missing_ok=True)

        # - Borrar notificaciones asociadas a la publicacion
        notificaciones = Notificacion.objects.filter(recurso=document)
        notificaciones.delete()

from app.models.peticion import Notificacion
class Comentario(db.Document):
    """
    Comentario de una publicacion
    """
    contenido = db.StringField()
    fecha = db.DateTimeField()
    respuestas = db.ListField(db.ReferenceField("self",
        # Borrar las respuestas del comentario si es borrado
        reverse_delete_rule=db.CASCADE)
    )
    usuario = db.ReferenceField("User")
    publicacion = db.ReferenceField(
        "Publicacion",
        # Este comentario se borra si la publicacion se borra
        reverse_delete_rule=db.CASCADE
    )

    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB

    def __str__(self) -> str:
        return f"{self.usuario} contenido={self.contenido}"
