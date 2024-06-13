from flask import Flask, jsonify
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to UDP Apuntes en Línea!"

@app.route('/test-db')
def test_db():
    try:
        users = User.query.all()
        return jsonify([user.email for user in users])
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
