from app import db
from app.constants import MAX_IMAGE_SIZE

class Publicacion(db.Document):
    contenido = db.StringField()
    tipo_publicacion = db.StringField()
    multimedia = db.FileField()
    imagenes = db.ListField(db.ImageField(size=MAX_IMAGE_SIZE))
    # Videos sera por los momentos una lista de urls
    videos = db.ListField(db.URLField())
    enlaces = db.ListField(db.URLField())
    fecha = db.DateTimeField()
    comentarios = db.ListField(db.ReferenceField("Comentario"))
    autor = db.ReferenceField("User")

class Comentario(db.Document):
    respuestas = db.ListField(db.ReferenceField("self"))
    publicacion = db.ReferenceField("Publicacion")
    contenido = db.StringField(max_length="800")
    usuario = db.ReferenceField("User")
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
