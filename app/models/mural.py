from app import db
from app.constants import MAX_IMAGE_SIZE

class Publicacion(db.Document):
    contenido = db.StringField()
    tipo_publicacion = db.StringField()
    fecha = db.DateTimeField()

    multimedia = db.FileField()
    imagenes = db.ListField(db.ImageField(size=MAX_IMAGE_SIZE))
    videos = db.ListField(db.URLField())

    enlaces = db.ListField(db.URLField())

    comentarios = db.ListField(db.ReferenceField("Comentario"))
    autor = db.ReferenceField("User")

class Comentario(db.Document):
    contenido = db.StringField()
    fecha = db.DateTimeField()
    
    respuestas = db.ListField(db.ReferenceField("self"))
    usuario = db.ReferenceField("User")
    publicacion = db.ReferenceField("Publicacion")
    
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB