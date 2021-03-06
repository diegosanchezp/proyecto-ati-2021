"""
Modulo de utils
"""
# Imports utilizado para tipos
from flask import Flask
from pathlib import Path
from typing import List
from app.constants import UPLOAD_EXTENSIONS
import os

def register_blueprints(app: Flask) -> None:
    """
    Registrar todos los blueprints en la app
    """
    # Importar blueprints
    from app.mural.vistas import mural_blueprint
    from app.chat.vistas import chat_blueprint
    from app.notificaciones.vistas import notificaciones_blueprint
    from app.usuario.vistas import usuario_blueprint, facebook_blueprint
    from app.media.vistas import media_blueprint

    # Registrar blueprints con la app de Flask
    app.register_blueprint(mural_blueprint, url_prefix="/mural")
    app.register_blueprint(chat_blueprint, url_prefix="/chat")
    app.register_blueprint(notificaciones_blueprint, url_prefix="/notificaciones")
    app.register_blueprint(usuario_blueprint, url_prefix="/")
    app.register_blueprint(media_blueprint, url_prefix="/media")
    app.register_blueprint(facebook_blueprint, url_prefix="/fb")

def register_signals() -> None:
    """
    Registrar signals de modelos
    """
    from mongoengine import signals
    from app.models.mural import Publicacion
    from app.models.peticion import Notificacion

    signals.post_delete.connect(Publicacion.post_delete, sender=Publicacion)
    signals.post_save.connect(Notificacion.post_save, sender=Notificacion)

def register_context_procesor(app: Flask) -> None:
    """
    Cargar variables o funciones al procesador de contexto de flask
    """

    @app.context_processor
    def inject_count_notificaciones():
        """
        Cargar una funcion, usable en templates
        para contar el numero de notificaciones
        """
        def count_notificaciones(user):
            """
            Contar numero de notificaciones de un usuario
            """
            from flask_login.mixins import AnonymousUserMixin
            from app.models.peticion import Notificacion
            # Check that the user is logged in
            if not isinstance(user, AnonymousUserMixin):
                return Notificacion.objects.get_notificaciones_usuario(user).count()

        return dict(count_notificaciones=count_notificaciones)
        
def before_request(app: Flask) -> None:
    """
    Funciones que se ejecutan antes de cada request, generalmente
    para establecer contexto global

    https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.before_request
    """

def get_upload_path(app) -> Path:
    return Path(app.root_path) / app.config["UPLOAD_FOLDER"]

def check_upload_folder(app: Flask) -> None:
    """
    Verificar que las carpetas de imagenes de modelos
    existan, si no crearlas
    """
    folders_to_check = [
        app.config["PUBLICACIONES_FOLDER"],
    ]

    upload_path = get_upload_path(app)

    # Verificar que el directorio de uploads exista, si no crearlo
    if not upload_path.is_dir():
        upload_path.mkdir()
        app.logger.info(f"{str(upload_path)} created")

    for folder in folders_to_check:
        folder_path = upload_path / folder
        if not folder_path.is_dir():
            folder_path.mkdir()
            app.logger.info(f"{str(folder_path)} created")

def allowed_file_extension(filename) -> bool:
    """
    Verificar que el nombre de un archivo tenga las
    extensiones correctas
    """
    from flask import current_app
    if not bool(filename): # Empty filename
        return False

    file_ext = os.path.splitext(filename)[1]
    return file_ext in UPLOAD_EXTENSIONS

def load_fixtures(app, user_manager) -> None:
    """
    Cargar cosas en base de datos si no existen,
    estos son requeridos para los test de la matriz de prueba
    """
    from app.models.user import User, USUARIO_GENEROS
    from datetime import datetime
    # Crear usuarios nuevos
    genero_masculino = USUARIO_GENEROS[0][0]
    password="Dev123456"

    aaron = User(
        ci=27449007,
        nombre="Aaron Morillo",
        username="aaron_morillo",
        email="aaron@mail.com",
        genero=genero_masculino,
        password=user_manager.hash_password(password),
        fecha_nacimiento=datetime(year=1999, month=10, day=1),
    )

    diego = User(
        ci=26334929,
        nombre="Diego S??nchez",
        username="diego_sanchez",
        email="diego@mail.com",
        genero=genero_masculino,
        password=user_manager.hash_password(password),
        fecha_nacimiento=datetime(year=1998, month=9, day=14),
    )

    try:
        User.objects.get(username=diego.username)
    except User.DoesNotExist:
        diego.save()
        app.logger.info(f"Usuario {diego.username} creado")
    try:
        User.objects.get(username=aaron.username)
    except User.DoesNotExist:
        aaron.save()
        app.logger.info(f"Usuario {aaron.username} creado")
        
def get_mime_types() -> List[str]:
    return [f"image/{_type.replace('.','')}" for _type in UPLOAD_EXTENSIONS]
