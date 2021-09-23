from app import db
from datetime import datetime, timedelta

class MensajeChat(db.Document):
    """
    Mensaje de un chat
    """
    # Si el emisor o receptor se borran el mensaje se borrara
    emisor = db.ReferenceField("User", reverse_delete_rule=db.CASCADE)
    receptor = db.ReferenceField("User", reverse_delete_rule=db.CASCADE)
    contenido = db.StringField()
    fecha_creacion = db.DateTimeField(default=datetime.today() - timedelta(hours=4))