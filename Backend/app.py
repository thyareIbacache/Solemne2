from flask import Flask
from Backend.config import Config
from Backend.models import db
from routes.auth import auth_bp
from routes.documents import documents_bp
from routes.search import search_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(documents_bp, url_prefix='/documents')
app.register_blueprint(search_bp, url_prefix='/search')

if __name__ == '__main__':
    app.run(debug=True)
