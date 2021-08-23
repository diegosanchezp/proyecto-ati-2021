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
    #videos = FieldList(URLFiield())
    enlaces = FieldList(StringField(_('Enlace')))

class SearchBarForm(FlaskForm):
    tipo_busqueda = SelectField('Tipo de busqueda', 
                            choices=[ ('amigo',_('Amigo')),
                                      ('desconocido',_('Desconocido')) ] )
    texto_busqueda = StringField('Persona a buscar')

class ComentarioForm(FlaskForm):
    contenido = TextAreaField('Contenido', [validators.Length(max=800)])
