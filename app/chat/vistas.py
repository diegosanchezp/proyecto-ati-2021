from flask import Blueprint, render_template, redirect, url_for
from flask_socketio import emit, join_room
import json
from app import socketio
from app.models.user import User
from app.models.chat import MensajeChat
from app.models.peticion import Notificacion, TipoNotificaciones
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
    newMessage = MensajeChat(contenido= decoded_data["mensaje"], receptor = decoded_data["receptorId"], emisor = current_user)
    newMessage.save()
    # Enviar notificacion de mensaje nuevo al receptor
    n = Notificacion(recurso=newMessage, descripcion=f"Mensaje nuevo de chat", emisor=current_user, receptor=decoded_data["receptorId"], tipo=TipoNotificaciones.MENSAJE_CHAT)
    n.save()
    emit("mensaje_privado", decoded_data["mensaje"], to=decoded_data["receptorId"])


@chat_blueprint.route("/<string:username>")
def index(username):
    """
    Vista principal del chat
    """
    receiver = User.objects.get_or_404(username= username)
    # Si no eres amigo no puedes chatear con esta persona
    if receiver not in current_user.amigos:
        redirect(location=url_for("mural_blueprint.index", page=1))
    messages = MensajeChat.objects(
        (Q(receptor=receiver.id) & Q(emisor=current_user.id)) \
        | (Q(receptor=current_user.id) & Q(emisor=receiver.id)))
    return render_template("chat/chat.html", receiver = receiver, messages = messages)
