from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .models import Archivos, db

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@upload_bp.route('/cargar', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        id_usuario = session['id_usuario']

        nombre_archivo = request.form.get('nombre_archivo')
        asignatura = request.form.get('asignatura')
        unidad = request.form.get('unidad')
        if not nombre_archivo or not asignatura or not unidad:
            mensaje = 'Por favor, completa todos los campos del formulario.'
            return render_template('upload.html', error_message=mensaje, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        if 'archivo' not in request.files:
            return 'No se encontró el archivo', 400

        file = request.files['archivo']

        if file.filename == '':
            mensaje = 'No se seleccionó ningun archivo.'
            return render_template('upload.html', error_message=mensaje, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        if file:
            # Guardar el archivo en el sistema de archivos del servidor
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            # Obtener la extensión del archivo para determinar su tipo
            file_extension = os.path.splitext(filename)[1][1:].lower()  # Obtener la extensión y convertir a minúsculas

            # Crear un nuevo objeto Archivos para almacenar en la base de datos
            nuevo_archivo = Archivos(
                nombre_archivo=request.form['nombre_archivo'],
                tipo=file_extension,
                fecha_subida=datetime.utcnow(),
                usuario_que_lo_subio=id_usuario,  # (ID del usuario actual)
                etiquetas='',
                ruta_archivo=os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                estado='pendiente',
                asignatura=request.form['asignatura'],
                unidad=request.form['unidad'],
            )

            # Agregar el nuevo archivo a la sesión de la base de datos
            db.session.add(nuevo_archivo)

            try:
                db.session.commit()
                return redirect(url_for('profile.perfil'))
            except Exception as e:
                return f'Error al guardar en la base de datos: {str(e)}', 500

    return render_template('upload.html')
