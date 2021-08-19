from wtforms import Form, BooleanField, StringField, FieldList,TextAreaField,FileField,SelectField, validators
from flask_babel import _



class PublicacionForm(Form):
    contenido = TextAreaField('', [validators.Length(max=1000)])
    tipo_publicacion = SelectField('', 
                            choices=[('',_('Tipo de Publicacion')),
                                     ('publica',_('Publica')),
                                     ('privada',_('Privada'))])

    # Multiple media files
    #imagenes = ListField(ImageField(size=MAX_IMAGE_SIZE))
    #videos = FieldList(URLFiield())
    multimedia = FileField('')
    enlaces = FieldList(StringField())

    #comentarios = FieldList(ReferenceField("Comentario"))
    #autor = ReferenceField("User")

class ComentarioForm(Form):
    #respuestas = FieldList(ReferenceField("self"))
    #publicacion = ReferenceField("Publicacion")
    contenido = StringField('Texto', [validators.Length(max=800)])
    #usuario = ReferenceField("User")
    # No se define un campo de fecha de creacion, esta
    # se obtendra utilizando el timestamp de mongoDB
