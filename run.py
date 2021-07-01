from dotenv import load_dotenv
from app import create_app

# Cargar variables de entorno
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)     # open for everyone
