from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .models import Archivos, Cursos, Archivos_Cursos, db

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()

    if request.method == 'POST':
        id_usuario = session['id_usuario']

        nombre_archivo = request.form.get('nombre_archivo')
        asignatura = request.form.get('curso')
        unidad = request.form.get('unidad')
        curso_seleccionado = request.form.get('curso')

        if not nombre_archivo or not asignatura or not unidad:
            mensaje = 'Por favor, completa todos los campos del formulario.'
            return render_template('upload.html', error_message=mensaje, curso_seleccionado=curso_seleccionado, cursos=cursos, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        if 'archivo' not in request.files:
            return 'No se encontró el archivo', 400

        file = request.files['archivo']

        if file.filename == '':
            mensaje = 'No se seleccionó ningun archivo.'
            return render_template('upload.html', error_message=mensaje, nombre_archivo=nombre_archivo, asignatura=asignatura, unidad=unidad)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            file_extension = os.path.splitext(filename)[1][1:].lower()

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
                auditado=False  # Inicialmente no auditado
            )

            db.session.add(nuevo_archivo)
            db.session.commit()

            nuevo_archivo_curso = Archivos_Cursos(
                id_archivo=Archivos.query.filter(
                    Archivos.nombre_archivo == nombre_archivo,
                    Archivos.usuario_que_lo_subio == id_usuario
                ).first().id_archivo,
                id_curso=Cursos.query.filter_by(nombre_curso=asignatura).first().id_curso
            )

            db.session.add(nuevo_archivo_curso)
            db.session.commit()

            return redirect(url_for('profile.perfil'))

    return render_template('upload.html', cursos=cursos)
