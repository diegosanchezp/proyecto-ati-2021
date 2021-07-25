from flask_user import UserMixin
from app import db

class User(db.Document, UserMixin):
    # User authentication information
    username = db.StringField(unique=True)
    password = db.StringField()
    nombre = db.StringField()
    foto = db.ImageField(size=(1024, 768, True))
    email = db.EmailField()
    ci = db.IntField(unique=True)
    fecha_nacimiento = db.DateTimeField()
    genero = db.StringField()
    descripcion = db.StringField()
    color = db.StringField()
    libro = db.StringField()
    musica = db.StringField()
    video_juegos = db.ListField()
    lenguajes_programacion = db.ListField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create username from nombre
        if self.username is None and self.nombre is not None:
            self.username = self.nombre.lower().replace(" ", "_")

    def __str__(self):
        return f"username={self.username} nombre={self.nombre} ci={self.ci}"
