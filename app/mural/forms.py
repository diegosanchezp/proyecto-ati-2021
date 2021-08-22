from wtforms import (
    BooleanField, StringField,
    FieldList,TextAreaField,
    SelectField, MultipleFileField,
    validators,
)

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from flask_babel import _
from app.models.mural import TIPO_PUBLICACIONES


class PublicacionForm(FlaskForm):
    contenido = TextAreaField(label=_('Contenido'), validators=[
        validators.Length(max=1000),
        validators.InputRequired(message=_("Error: publicación vacía"))])

    tipo_publicacion = SelectField(_('Tipo de publicacion'),choices=TIPO_PUBLICACIONES)

    # Multiple media files
    images = MultipleFileField(label=_("Imágenes"))
    #imagenes = ListField(ImageField(size=MAX_IMAGE_SIZE))
    #videos = FieldList(URLFiield())
    enlaces = FieldList(StringField(_('Enlace')))

    #comentarios = FieldList(ReferenceField("Comentario"))
    #autor = ReferenceField("User")

class SearchBarForm(FlaskForm):
    tipo_busqueda = SelectField('Tipo de busqueda', 
                            choices=[ ('amigo',_('Amigo')),
                                      ('desconocido',_('Desconocido')) ] )
    texto_busqueda = StringField('Persona a buscar')

class ComentarioForm(FlaskForm):
    #respuestas = FieldList(ReferenceField("self"))
    #publicacion = ReferenceField("Publicacion")
    contenido = StringField('Texto', [validators.Length(max=800)])
    #usuario = ReferenceField("User")
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
