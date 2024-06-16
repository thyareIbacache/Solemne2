from flask import Flask, session, render_template, request, redirect, url_for,  send_from_directory
from config import Config
from models import db, Usuarios, Archivos
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from datetime import datetime


app = Flask(__name__, template_folder='HTML')
app.config.from_object(Config)
db.init_app(app)

# ruta de carga de archivos
UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamaño máximo del archivo (en bytes)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        usuario = Usuarios.query.get(id_usuario)
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
        return redirect(url_for('perfil'))
    
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']

        usuario = Usuarios.query.filter_by(correo=correo).first()

        if usuario and (usuario.contraseña == contraseña):
            session['id_usuario'] = usuario.id_usuario
            return redirect(url_for('perfil', id_usuario=usuario.id_usuario))
        else:
            mensaje = 'Credenciales inválidas'
            #if usuario:
            #    mensaje += f'. La contraseña correcta es: {usuario.contraseña}'
            return mensaje
            #return render_template('Login.html', error_message=mensaje)

    return render_template('Login.html')

# Función para validar el formulario de carga de archivos
def validar_formulario(request):
    nombre_archivo = request.form.get('nombre_archivo')
    asignatura = request.form.get('asignatura')
    unidad = request.form.get('unidad')

    if not nombre_archivo or not asignatura or not unidad:
        return False, 'Por favor, completa todos los campos del formulario.'

    return True, ''

# Ruta para la carga de archivos
@app.route('/cargar', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        id_usuario = session['id_usuario']
        # Validar el formulario antes de procesar la carga de archivos
        valido, mensaje_error = validar_formulario(request)
        if not valido:
            return mensaje_error, 400

        # Verificar si se ha enviado un archivo en la solicitud
        if 'archivo' not in request.files:
            return 'No se encontró el archivo', 400

        file = request.files['archivo']

        # Verificar si no se seleccionó ningún archivo
        if file.filename == '':
            return 'No se seleccionó ningún archivo', 400

        # Si se recibe un archivo y es válido
        if file:
            # Guardar el archivo en el sistema de archivos del servidor
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Obtener la extensión del archivo para determinar su tipo
            file_extension = os.path.splitext(filename)[1][1:].lower()  # Obtener la extensión y convertir a minúsculas

            # Crear un nuevo objeto Archivos para almacenar en la base de datos
            nuevo_archivo = Archivos(
                nombre_archivo=request.form['nombre_archivo'],
                tipo=file_extension,
                fecha_subida=datetime.utcnow(),
                usuario_que_lo_subio=id_usuario,  # (ID del usuario actual)
                etiquetas='',
                ruta_archivo=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                estado='pendiente',
                asignatura=request.form['asignatura'],
                unidad=request.form['unidad'],
            )

            # Agregar el nuevo archivo a la sesión de la base de datos
            db.session.add(nuevo_archivo)

            try:
                # Confirmar los cambios en la base de datos
                db.session.commit()
                return redirect(url_for('perfil'))
            except Exception as e:
                # Manejar cualquier error que pueda ocurrir al guardar en la base de datos
                return f'Error al guardar en la base de datos: {str(e)}', 500

    # Si se accede a la página de carga de archivos por GET o si hay errores en POST, renderizar el formulario
    return render_template('Cargarv2.html')

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
