from flask import Flask, session, render_template, request, redirect, url_for, send_from_directory,jsonify
from config import Config
from models import db, Usuarios, Archivos
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from authlib.integrations.flask_client import OAuth
from datetime import datetime
import os

app = Flask(__name__, template_folder='HTML')
app.config.from_object(Config)
db.init_app(app)

# Ruta de carga de archivos
UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamaño máximo del archivo (en bytes)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'id_usuario' in session:
        return redirect(url_for('perfil'))
    
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']
        usuario = Usuarios.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['id_usuario'] = usuario.id_usuario
            return redirect(url_for('perfil'))
        else:
            mensaje = 'Credenciales inválidas'
            return render_template('Login.html', error_message=mensaje, username=correo)
    
    error_message = request.args.get('error', None)
    if error_message:
        return render_template('Login.html', error_message=error_message)

    return render_template('Login.html')

oauth = OAuth(app)
google = oauth.register(
    'google',
    server_metadata_url=os.getenv('GOOGLE_METADATA_URL'),  # Asegúrate de que estas variables estén definidas en otro lugar
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/cargar', methods=['GET', 'POST'])
def cargar():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(id_usuario))
        os.makedirs(user_upload_folder, exist_ok=True)  # Crear carpeta si no existe

        if request.method == 'POST':
            archivo = request.files['archivo']
            if archivo:
                filename = secure_filename(archivo.filename)
                archivo.save(os.path.join(user_upload_folder, filename))  # Guardar en la carpeta del usuario

                # Guardar en la base de datos
                nuevo_archivo = Archivos(
                    nombre_archivo=filename,
                    fecha_subida=datetime.now(),
                    usuario_que_lo_subio=id_usuario,
                    etiquetas='',
                    ruta_archivo=os.path.join(user_upload_folder, filename),
                    estado='pendiente',
                    asignatura=request.form['asignatura'],
                    unidad=request.form['unidad'],
                )
                db.session.add(nuevo_archivo)
                try:
                    db.session.commit()
                    return redirect(url_for('perfil'))
                except Exception as e:
                    return f'Error al guardar en la base de datos: {str(e)}', 500
        return render_template('Cargarv2.html')
    return redirect(url_for('home'))

@app.route('/perfil')
def perfil():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        usuario = Usuarios.query.get(id_usuario)
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
        return render_template('PerfilWebv3.html', usuario=usuario, archivos=archivos)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    return redirect(url_for('home'))

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
