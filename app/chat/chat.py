from flask import Blueprint, render_template
chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')

@chat_blueprint.route("/")
def index():
    return "Futuro Chat"
