from wtforms import validators, fields, widgets
from wtforms.fields import html5 as html5_fields
from wtforms.widgets import html5 as html5_widgets
from flask_babel import _
from app.models.user import (
    USUARIO_GENEROS, User,
    UserConfig,
    LANGUAGES,
)
from app.usuario.custom_fields import StringListField, ImageField
from app.models.user import User, UserConfig

from flask_user.forms import (
    RegisterForm as CoreRegisterForm,
    LoginForm as CoreLoginForm,
    EditUserProfileForm as CoreEditUserProfileForm
)

from app.models.user import ( UserConfig, UserNotificationsConfig )

from flask_wtf import FlaskForm as CoreConfigForm
from flask_mongoengine.wtf.orm import model_form

ConfigForm = model_form(
    model=UserConfig,field_args={
        "color_perfil": { "widget": html5_widgets.ColorInput() },
        "color_muro": { "widget": html5_widgets.ColorInput() }
    }
)

PrivacyForm =  model_form(
    model=UserConfig,
    exclude=("color_perfil", "color_muro", "notificaciones","lenguaje")
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
        default=False,
    )
