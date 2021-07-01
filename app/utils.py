"""
Modulo de utils
"""
# Importar blueprints


def register_blueprints(app):
    # Importar blueprints
    from app.mural.vistas import mural_blueprint
    from app.chat.chat import chat_blueprint

    # Registrar blueprints con la app de Flask
    app.register_blueprint(mural_blueprint, url_prefix="/mural")
    app.register_blueprint(chat_blueprint, url_prefix="/chat")
