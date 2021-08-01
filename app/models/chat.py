class MensajeChat(db.Document):
    emisor = db.ReferenceField("User")
    receptor = db.ReferenceField("User")
    contenido = db.StringField()
