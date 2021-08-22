from app import db
from app.constants import MAX_IMAGE_SIZE
from flask_babel import _
from typing import List
from flask import url_for
TIPO_PUBLICACIONES = [
    ("PUBLICA", _("Publica")),
    ("PRIVADA", _("Privada")),
]

class Publicacion(db.Document):
    contenido = db.StringField()
    tipo_publicacion = db.StringField(choices=TIPO_PUBLICACIONES)
    multimedia = db.FileField()
    # Arreglo de nombre de imagenes
    imagenes = db.ListField(db.StringField())
    # Videos sera por los momentos una lista de urls
    videos = db.ListField(db.URLField())
    enlaces = db.ListField(db.URLField())
    fecha = db.DateTimeField()
    comentarios = db.ListField(db.ReferenceField("Comentario"))
    autor = db.ReferenceField("User")

    def __str__(self) -> str:
        return f"autor={self.autor} contenido={self.contenido}"

    def get_image_urls(self) -> List[str]:
        """
        Obtener urls para las imagenes de esta publicacion
        """
        return [url_for("media_blueprint.foto_publicacion", file_name=img_name) for img_name in self.imagenes]

class Comentario(db.Document):
    respuestas = db.ListField(db.ReferenceField("self"))
    publicacion = db.ReferenceField("Publicacion")
    contenido = db.StringField(max_length="800")
    usuario = db.ReferenceField("User")
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
