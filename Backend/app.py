from flask import Flask, jsonify, render_template
from config import Config
from models import db, Usuarios

app = Flask(__name__, template_folder='HTML')
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('Login.html')

@app.route('/cargar')
def cargar():
    return render_template('Cargar.html')

@app.route('/perfil')
def perfil():
    return render_template('PerfilWebv2.html')

@app.route('/test-db')
def test_db():
    try:
        users = Usuarios.query.all()
        user_data = [
            {
                'id_usuario': user.id_usuario,
                'correo': user.correo,
                'fecha_registro': user.fecha_registro,
                'rol': user.rol
            } for user in users
        ]
        return jsonify(user_data)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
