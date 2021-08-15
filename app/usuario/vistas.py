from flask import Blueprint, render_template
from app.models.user import USUARIO_GENEROS
from flask_login import current_user
usuario_blueprint = Blueprint('usuario_blueprint', __name__, template_folder='templates')
from app.models.user import User

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

@usuario_blueprint.route("/ver-perfil/<username>")
def ver_perfil(username):
    """
    Vista de ver perfil
    """
    target_user = User.objects(username=username).first()
    target_user_format = {
        'nombre' : target_user.nombre,
        'email' : target_user.email,
        'foto' : target_user.get_foto_url(),
        'ci' :  target_user.ci,
        'fecha_nacimiento' : target_user.fecha_nacimiento,
        'genero' : USUARIO_GENEROS[1][1] if target_user.genero=='F' else USUARIO_GENEROS[0][1],
        'descripcion' : target_user.descripcion,
        'color' : target_user.color,
        'video_juegos' : ', '.join(target_user.video_juegos),
        'lenguajes_programacion' : ', '.join(target_user.lenguajes_programacion)
        } 

    it_is_the_current_user = False
    if target_user.username == current_user.username:
        it_is_the_current_user = True
    
    return render_template("usuario/ver_perfil.html", target_user = target_user_format, it_is_the_current_user = it_is_the_current_user)

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
