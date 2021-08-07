from wtforms import validators, fields, widgets
from wtforms.fields import html5 as html5_fields
from wtforms.widgets import html5 as html5_widgets
from flask_babel import _
from app.models.user import USUARIO_GENEROS
from app.usuario.custom_fields import StringListField, ImageField

from flask_user.forms import (
    RegisterForm as CoreRegisterForm,
    LoginForm as CoreLoginForm,
    EditUserProfileForm as CoreEditUserProfileForm
)

class RegisterForm(CoreRegisterForm):
    nombre = fields.StringField(
        label=_("Nombre"),
        validators=[validators.InputRequired(message=_("Nombre Requirido"))]
    )
    ci = html5_fields.IntegerField(label=_("Cédula de identidad"),
        validators=[validators.InputRequired(message=_("Cédula requerida"))]
    )

    fecha_nacimiento = html5_fields.DateField(label=_("Fecha de nacimiento"),
        validators=[validators.InputRequired(message=_("Fecha de nacimiento requerida"))]
    )

    genero = fields.SelectField(label=_("Género"),
        validators=[validators.InputRequired(message=_("Género requerido"))],
        choices=USUARIO_GENEROS
    )

class LoginForm(CoreLoginForm):
    #No se hacen cambios
    pass
    

class EditUserProfileForm(CoreEditUserProfileForm):
    """Customized Edit user profile form"""

    first_name = fields.StringField(
        label=_("Primer nombre")
        )
    last_name = fields.StringField(
        label=_("Apellido")
        )
    nombre = fields.StringField(
        label=_("Nombre"),
         validators=[validators.DataRequired()]
        )
    ci = html5_fields.IntegerField(
        label=_('Cédula de identidad'),
        validators=[validators.DataRequired()]
        )
    genero = fields.SelectField(
        label=_("Género"),
        validators=[validators.InputRequired(message=_("Género requerido"))],
        choices=USUARIO_GENEROS
    )
    foto = ImageField(

    )
    email = fields.StringField(
        label=_("Correo electrónico"),
        render_kw={'disabled':''}
        )
    fecha_nacimiento = html5_fields.DateField(
        label=_("Fecha de nacimiento")
    )
    descripcion = fields.TextAreaField(
        label=_("Descripción")
    )
    color = fields.StringField(
        label=_("Color favorito")
    )
    libro = fields.StringField(
        label=_("Libro favorito")
    )
    musica = fields.StringField(
        label=_("Música favorita")
    )
    video_juegos = StringListField(
        label=_("Video Juegos favoritos")
    )   
    lenguajes_programacion = StringListField(
        label=_("Lenguajes de programación conocidos")
    )

