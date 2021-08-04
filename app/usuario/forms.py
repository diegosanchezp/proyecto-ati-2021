from wtforms import validators, fields
from wtforms.fields import html5
from flask_babel import _
from app.models.user import User, USUARIO_GENEROS

from flask_user.forms import (
    RegisterForm as CoreRegisterForm,
    LoginForm as CoreLoginForm,
)

class RegisterForm(CoreRegisterForm):
    nombre = fields.StringField(
        label=_("Nombre"),
        validators=[validators.InputRequired(message=_("Nombre Requirido"))]
    )
    ci = html5.IntegerField(label=_("Número cédula de identidad"),
        validators=[validators.InputRequired(message=_("Cédula requerida"))]
    )

    fecha_nacimiento = html5.DateField(label=_("Fecha de nacimiento"),
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
    #Creo que no hace falta customizarlo
    pass
