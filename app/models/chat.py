class MensajeChat(db.Document):
    """
    Mensaje de un chat
    """
    # Si el emisor o receptor se borran el mensaje se borrara
    emisor = db.ReferenceField("User", reverse_delete_rule=db.CASCADE)
    receptor = db.ReferenceField("User", reverse_delete_rule=db.CASCADE)
    contenido = db.StringField()
