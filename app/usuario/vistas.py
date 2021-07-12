from flask import Blueprint, render_template
usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')

@usuario_blueprint.route("/")
def index():
    """
    Login, vista principal
    """
    return render_template("usuario/login.html")

@usuario_blueprint.route("/registro")
def registro():
    """
    Pagina de Registro
    """
    return render_template("usuario/registro.html")

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

@usuario_blueprint.route("/editar-perfil")
def editar_perfil():
    """
    Vista de editar perfil
    """

    return render_template("usuario/editar_perfil.html")

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
