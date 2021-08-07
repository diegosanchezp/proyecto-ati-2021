from flask import Blueprint, render_template
usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User

@usuario_blueprint.route("/borrar-db")
def borrar_db():
    """
    Vista de recuperación de contraseña
    """
    User.objects().delete()
    return "Borrada!"

@usuario_blueprint.route("/ver-db")
def ver_db():
    """
    Vista de recuperación de contraseña
    """
    user = User.objects().first()
    print(user.foto)
    return "Vista!"



@usuario_blueprint.route("/recuperar")
def recuperar_password():
    """
    Vista de recuperación de contraseña
    """

    return render_template("usuario/recuperar_password.html")

@usuario_blueprint.route("/recuperar-token")
def recuperar_token():
    """
    Vista de recuperación de contraseña
    """

    return render_template("usuario/recuperar_pass_token_enviado.html")

@usuario_blueprint.route("/ver-perfil")
def ver_perfil():
    """
    Vista de ver perfil
    """
    return render_template("usuario/ver_perfil.html")
@usuario_blueprint.route("/editar-password")
def editar_password():
    """
    Vista de editar password
    """

    return render_template("usuario/editar_password.html")

@usuario_blueprint.route("/editar-privacidad")
def editar_privacidad():
    """
    Vista de editar privacidad
    """

    return render_template("usuario/editar_privacidad.html")

@usuario_blueprint.route("/configuracion")
def configuracion():
    """
    Vista de configuracion
    """

    return render_template("usuario/configuracion.html")

@usuario_blueprint.route("/mis-amigos")
def mis_amigos():
    """
    Mis amigos
    """
    return render_template("usuario/mis_amigos.html")

@usuario_blueprint.route("/mi-perfil")
def mi_perfil():
    """
    Mi perfil
    """
    return render_template("usuario/mi_perfil.html")
