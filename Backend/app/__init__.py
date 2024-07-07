from flask import Flask
from .config import Config
from .routes.models import db
from .routes.auth import auth_bp
from .routes.profile import profile_bp
from .routes.upload import upload_bp
from .routes.biblioteca import biblioteca_bp
from .routes.anuncios import anuncios_bp
from .routes.admin import admin_bp
from .routes.auditoria import auditoria_bp
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
        client_kwargs={'scope': 'openid email profile', 'prompt': 'consent'}
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(biblioteca_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auditoria_bp)
    return app
