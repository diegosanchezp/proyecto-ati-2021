from flask import Blueprint, render_template
from flask_socketio import emit, join_room
import json
from app import socketio
from app.models.user import User
from app.models.chat import MensajeChat
from flask_user import current_user
from mongoengine.queryset.visitor import Q
import datetime

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
    emit("room_joined", "connected", to=decoded_data["emisorId"])

@socketio.on('message')
def handle_message(data: str):
    """
    Enviar mensaje a la room privada de unos de tus amigos
    """
    decoded_data = json.loads(data)
    newMessage = MensajeChat(contenido= decoded_data["mensaje"], receptor = decoded_data["receptorId"], emisor = decoded_data["emisorId"])
    newMessage.save()
    emit("mensaje_privado", decoded_data["mensaje"], to=decoded_data["receptorId"])


@chat_blueprint.route("/<username>")
def index(username):
    """
    Vista principal del chat
    """
    receiver = User.objects.get_or_404(username= username)
    messages = MensajeChat.objects(Q(receptor = receiver.id) | Q(receptor = current_user.id) & Q(emisor = receiver.id) | Q(emisor = current_user.id))
    return render_template("chat/chat.html", receiver = receiver, messages = messages)
