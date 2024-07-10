from flask import Flask
from .config import Config
from .routes.models import db
from .routes.auth import auth_bp
from .routes.profile import profile_bp
from .routes.upload import upload_bp
from .routes.biblioteca import biblioteca_bp
from .routes.anunciosA import anunciosA_bp
from .routes.anunciosE import anunciosE_bp
from .routes.admin import admin_bp
from .routes.auditoria import auditoria_bp

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.
    
    Returns:
        Flask: La instancia de la aplicación configurada.
    """
    # Crear la aplicación Flask
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Configurar la aplicación con la configuración especificada en Config
    app.config.from_object(Config)
    
    # Inicializar la base de datos con la aplicación
    db.init_app(app)

    # Configuración de OAuth para autenticación con Google
    oauth = OAuth(app)
    app.oauth = oauth

    google = oauth.register(
        'google',
        server_metadata_url=os.getenv('GOOGLE_METADATA_URL'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        client_kwargs={'scope': 'openid email profile', 'prompt': 'consent'}
    )

    # Registrar blueprints para cada módulo de la aplicación
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(biblioteca_bp)
    app.register_blueprint(anunciosA_bp)
    app.register_blueprint(anunciosE_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auditoria_bp)

    return app
