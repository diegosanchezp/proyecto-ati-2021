from wtforms import (
    BooleanField, StringField,
    FieldList,TextAreaField,
    SelectField, MultipleFileField,
    validators, Form
)

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from app.utils import get_mime_types
from flask_babel import _
from app.models.mural import TIPO_PUBLICACIONES

from flask import current_app as app

class PublicacionForm(FlaskForm):
    contenido = TextAreaField(label=_('Contenido'), validators=[
        validators.Length(max=1000, message=_("Solo 1000 caracteres son permitidos")),
        validators.InputRequired(message=_("Error: publicación vacía"))])

    tipo_publicacion = SelectField(_('Tipo de publicacion'),choices=TIPO_PUBLICACIONES)

    # Multiple media files
    images = MultipleFileField(label=_("Imágenes"), render_kw={
        "accept": ", ".join(get_mime_types())
    })
    #videos = FieldList(URLFiield())
    enlaces = FieldList(StringField(_('Enlace')))

class SearchBarForm(FlaskForm):
    tipo_busqueda = SelectField('Tipo de busqueda', 
                            choices=[ ('amigo',_('Amigo')),
                                      ('desconocido',_('Desconocido')) ] )
    texto_busqueda = StringField('Persona a buscar')

class ComentarioForm(Form):
    contenido = TextAreaField(label=_('Contenido'),
                              validators=[
                               validators.Length(max=800),
                               validators.InputRequired(message=_("Error: publicación vacía"))
                               ]
                              )
