from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .models import Archivos, Cursos, Archivos_Cursos, db

# Creación del Blueprint para manejar las rutas relacionadas con la carga de archivos
upload_bp = Blueprint('upload', __name__)

# Ruta para servir archivos subidos desde el directorio configurado
@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Ruta para manejar la carga de archivos (GET y POST)
@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Obtener todos los nombres de cursos disponibles desde la base de datos
    cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()

    if request.method == 'POST':  # Si la solicitud es un POST (se envió el formulario)
        id_usuario = session['id_usuario']  # Obtener el ID de usuario desde la sesión

        # Obtener los datos del formulario
        nombre_archivo = request.form.get('nombre_archivo')
        asignatura = request.form.get('curso')
        unidad = request.form.get('unidad')
        curso_seleccionado = request.form.get('curso')

        # Verificar que todos los campos del formulario estén completos
        if not nombre_archivo or not asignatura or not unidad:
            mensaje = 'Por favor, completa todos los campos del formulario.'
            return render_template('upload.html', error_message=mensaje, curso_seleccionado=curso_seleccionado, cursos=cursos, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        # Verificar si se incluyó un archivo en la solicitud
        if 'archivo' not in request.files:
            return 'No se encontró el archivo', 400

        file = request.files['archivo']  # Obtener el archivo de la solicitud

        # Verificar que se seleccionó un archivo para subir
        if file.filename == '':
            mensaje = 'No se seleccionó ningún archivo.'
            return render_template('upload.html', error_message=mensaje, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        # Procesar el archivo si se seleccionó uno
        if file:
            filename = secure_filename(file.filename)  # Asegurar el nombre del archivo
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))  # Guardar el archivo en el directorio configurado

            file_extension = os.path.splitext(filename)[1][1:].lower()  # Obtener la extensión del archivo

            # Crear un nuevo registro de archivo en la base de datos
            nuevo_archivo = Archivos(
                nombre_archivo=request.form['nombre_archivo'],
                id_curso=Cursos.query.filter_by(nombre_curso=asignatura).first().id_curso,
                tipo=file_extension,
                fecha_subida=datetime.utcnow(),
                usuario_que_lo_subio=id_usuario,
                etiquetas='',
                ruta_archivo=os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                estado='pendiente',
                asignatura=asignatura,
                unidad=request.form['unidad'],
            )

            db.session.add(nuevo_archivo)  # Agregar el nuevo archivo a la sesión de la base de datos
            db.session.commit()  # Confirmar los cambios en la base de datos

            # Asociar el archivo con el curso seleccionado
            nuevo_archivo_curso = Archivos_Cursos(
                id_archivo=Archivos.query.filter(
                    Archivos.nombre_archivo == nombre_archivo,
                    Archivos.usuario_que_lo_subio == id_usuario
                ).first().id_archivo,
                id_curso=Cursos.query.filter_by(nombre_curso=asignatura).first().id_curso
            )

            db.session.add(nuevo_archivo_curso)  # Agregar la asociación a la sesión de la base de datos
            db.session.commit()  # Confirmar los cambios en la base de datos

            return redirect(url_for('profile.perfil'))  # Redirigir al perfil del usuario después de una carga exitosa

    # Renderizar el formulario de carga de archivos
    return render_template('upload.html', cursos=cursos)
