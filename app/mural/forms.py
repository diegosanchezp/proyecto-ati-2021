from wtforms import Form, BooleanField, StringField, FieldList,TextAreaField,FileField,SelectField, validators
from flask_babel import _



class PublicacionForm(Form):
    contenido = TextAreaField('Contenido', [validators.Length(max=1000)])
    tipo_publicacion = SelectField('Tipo de publicacion', 
                            choices=[ ('publica',_('Publica')),
                                      ('privada',_('Privada')) ] )

    # Multiple media files
    #imagenes = ListField(ImageField(size=MAX_IMAGE_SIZE))
    #videos = FieldList(URLFiield())
    multimedia = FileField('Multimedia')
    enlaces = FieldList(StringField('Enlace'))

    #comentarios = FieldList(ReferenceField("Comentario"))
    #autor = ReferenceField("User")

class SearchBarForm(Form):
    tipo_busqueda = SelectField('Tipo de busqueda', 
                            choices=[ ('amigo',_('Amigo')),
                                      ('desconocido',_('Desconocido')) ] )
    texto_busqueda = StringField('Persona a buscar')

class ComentarioForm(Form):
    #respuestas = FieldList(ReferenceField("self"))
    #publicacion = ReferenceField("Publicacion")
    contenido = StringField('Texto', [validators.Length(max=800)])
    #usuario = ReferenceField("User")
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
