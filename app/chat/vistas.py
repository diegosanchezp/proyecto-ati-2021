from flask import Blueprint, render_template
from flask_socketio import emit, join_room
import json
from app import socketio
from app.models.user import User

chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')

@socketio.on('join')
def join(data):
    """
    Crear una room para el current user, para que tus amigos
    se puedan unir y chatear contigo
    """
    decoded_data = json.loads(data)
    room = decoded_data["emisorId"]
    join_room(room)
    emit("room_joined", "dude jount", to=decoded_data["emisorId"])

@socketio.on('message')
def handle_message(data: str):
    """
    Enviar mensaje a la room privada de unos de tus amigos
    """
    decoded_data = json.loads(data)
    print(decoded_data)
    emit("mensaje_privado", decoded_data["mensaje"], to=decoded_data["receptorId"])


@chat_blueprint.route("/<string:username>")
def index(username):
    """
    Vista principal del chat
    """
    receptor = User.objects.get_or_404(username=username)
    return render_template("chat/chat.html",
        receptor=receptor
    )
