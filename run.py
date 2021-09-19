from dotenv import load_dotenv
from app import create_app
from app import socketio
# Cargar variables de entorno
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)     # open for everyone
