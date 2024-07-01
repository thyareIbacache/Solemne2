from flask import Flask
from .config import Config
from .models import db
from .auth import auth_bp
from .profile import profile_bp
from .upload import upload_bp
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    
    db.init_app(app)

    # Configuración de OAuth
    oauth = OAuth(app)
    app.oauth = oauth

    google = oauth.register(
        'google',
        server_metadata_url=os.getenv('GOOGLE_METADATA_URL'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        client_kwargs={'scope': 'openid email profile'}
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(upload_bp)

    # Configuración de la carpeta de subida
    UPLOAD_FOLDER = './uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamaño máximo del archivo (en bytes)

    return app
