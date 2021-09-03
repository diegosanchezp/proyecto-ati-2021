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
    autor = db.ReferenceField("User")

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
        Borrar images cuando la publicacion se borre
        """
        imgs_path = cls.get_images_path()

        for img_name in document.imagenes:
            file_path = imgs_path / img_name
            file_path.unlink(missing_ok=True)

class Comentario(db.Document):
    contenido = db.StringField()
    fecha = db.DateTimeField()
    
    respuestas = db.ListField(db.ReferenceField("self"))
    usuario = db.ReferenceField("User")
    publicacion = db.ReferenceField("Publicacion")
    
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
