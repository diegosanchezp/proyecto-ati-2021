from flask import Blueprint, render_template
chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')
from app import socketio
import json

@socketio.on('message')
def handle_message(data: str):
    print(json.loads(data))

@chat_blueprint.route("/<string:username>")
def index(username):
    """
    Vista principal del chat
    """
    return render_template("chat/chat.html")
