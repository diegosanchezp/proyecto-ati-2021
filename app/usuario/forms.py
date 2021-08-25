from wtforms import validators, fields, widgets
from wtforms.fields import html5 as html5_fields
from wtforms.widgets import html5 as html5_widgets
from flask_babel import _
from app.models.user import USUARIO_GENEROS, LANGUAGES
from app.usuario.custom_fields import StringListField, ImageField
from app.models.user import User

from flask_user.forms import (
    RegisterForm as CoreRegisterForm,
    LoginForm as CoreLoginForm,
    EditUserProfileForm as CoreEditUserProfileForm
)

from app.models.user import ( UserConfig, UserNotificationsConfig )

from flask_wtf import FlaskForm as CoreConfigForm
from flask import current_app as app


class ConfigForm(CoreConfigForm):
    """
    Formulario de configuracion
    """

    emailFriend = fields.BooleanField(
        label=_(""), render_kw={'checked': UserNotificationsConfig().amigos_conectados}
    )

    emailNotification = fields.BooleanField(
        label=_(""), render_kw={'checked': UserNotificationsConfig().comentarios}
    )

    emailMessage = fields.BooleanField(
        label=_(""), render_kw={'checked': UserNotificationsConfig().mensajes_chat}
    )

    colorProfile = fields.StringField(label=_(""),widget=html5_widgets.ColorInput(), default=UserConfig().color_perfil)

    colorWall = fields.StringField(label=_(""),widget=html5_widgets.ColorInput(), default=UserConfig().color_muro)

    language = fields.SelectField(label=_(""),
        choices=LANGUAGES
    )

    privateProfile = fields.BooleanField(
        label=_(""), render_kw={'checked': UserConfig().perfil_privado}
    )

    privatePublications = fields.BooleanField(
        label=_(""), render_kw={'checked': UserConfig().publicaciones_privadas}
    )



class RegisterForm(CoreRegisterForm):
    """
    Formulario de registro extendido

    Warning:
    Los nombres de los fields que se guardan en bd
    tienen que ser los mismos de los del modelo de usuario
    """

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

    def populate_obj(self, obj):
        super().populate_obj(obj)
        if isinstance(obj, User):
            obj.set_username_from_nombre()

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
    genero = fields.SelectField(label=_("Género"),
        validators=[validators.InputRequired(message=_("Género requerido"))],
        choices=USUARIO_GENEROS
    )

    nombre_foto = fields.FileField(
        label=_("Foto de perfil"),
        validators=[]
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

    delete_foto = fields.BooleanField(
        label=_("¿ Borrar foto ?"),
    )
