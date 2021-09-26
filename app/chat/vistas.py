from flask import Blueprint, render_template, redirect, url_for, request
from flask_babel import _
from flask_socketio import emit, join_room, leave_room
import json
from app import socketio
from app.models.user import User
from app.models.chat import MensajeChat
from app.models.peticion import Notificacion, TipoNotificaciones
from flask_user import current_user
from mongoengine.queryset.visitor import Q
import datetime

chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')

@socketio.on('crear_room')
def join(data):
    """
    Crear una room para el current user, para que tus amigos
    se puedan unir y chatear contigo
    """

    room = str(current_user.id)
    join_room(room)
    emit("room_creada", "connected")

@socketio.on('conectar_con_amigo')
def conectar_con_amigo(data):
    """
    Notificar al receptor de los mensajes que el current_user
    esta conectado
    """

    decoded_data = json.loads(data)
    emit("amigo_conectado", _("%(nombre)s se ha conectado", nombre=current_user.nombre),to=decoded_data["receptorId"])

@socketio.on('message')
def handle_message(data: str):
    """
    Enviar mensaje a la room privada de unos de tus amigos
    """
    decoded_data = json.loads(data)
    print(decoded_data)
    # Mensajes se guardan en base de datos, para tener un historial
    newMessage = MensajeChat(contenido= decoded_data["mensaje"], receptor = decoded_data["receptorId"], emisor = current_user)
    newMessage.save()

    # Enviar notificacion de mensaje nuevo al receptor si esta desconectado
    if not decoded_data["receptorConectado"]:
        n = Notificacion(recurso=newMessage, descripcion=f"Mensaje nuevo de chat", emisor=current_user, receptor=decoded_data["receptorId"], tipo=TipoNotificaciones.MENSAJE_CHAT)
        n.save()

    emit("mensaje_privado", decoded_data["mensaje"], to=decoded_data["receptorId"])

@socketio.on('disconnect')
def test_disconnect():
    print(request)

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
