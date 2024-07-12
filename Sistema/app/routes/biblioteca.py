from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, db, Cursos
from datetime import datetime

# Definición del Blueprint para la biblioteca
biblioteca_bp = Blueprint('biblioteca', __name__)

# Ruta para la biblioteca general
@biblioteca_bp.route('/biblioteca')
def biblioteca():
    # Consulta para obtener todos los archivos aprobados
    archivos = Archivos.query.filter_by(estado="aprobado").all()
    # Consulta para obtener todos los cursos
    cursos = Cursos.query.all()
    # Renderiza la plantilla 'biblioteca.html' pasando los archivos y cursos como contexto
    return render_template('biblioteca.html', archivos=archivos, cursos=cursos)

# Ruta para la biblioteca de un curso específico
@biblioteca_bp.route('/biblioteca-cursos-<int:id_curso>')
def biblioteca_cursos(id_curso):
    # Consulta para obtener todos los archivos aprobados de un curso específico
    archivos = Archivos.query.filter_by(id_curso=id_curso, estado="aprobado").all()
    # Consulta para obtener el nombre del curso específico
    nombre_curso = Cursos.query.filter_by(id_curso=id_curso).first().nombre_curso
    # Consulta para obtener todos los cursos
    cursos = Cursos.query.all()
    # Renderiza la plantilla 'bibliocursos.html' pasando los archivos, nombre del curso y cursos como contexto
    return render_template('bibliocursos.html', archivos=archivos, nombre_curso=nombre_curso, cursos=cursos)

# Ruta para archivos compartidos por un usuario específico o por el usuario en sesión
@biblioteca_bp.route('/shared')
@biblioteca_bp.route('/shared-<int:id_usuario>')
def shared(id_usuario):
    # Verifica si hay un usuario en sesión
    if 'id_usuario' in session:
        # Si no se especifica un id_usuario, se utiliza el id_usuario de la sesión
        if id_usuario is None:
            id_usuario = session['id_usuario']
        # Consulta para obtener los datos del usuario
        usuario = Usuarios.query.filter_by(id_usuario=id_usuario).first()
        # Verifica si el usuario en sesión es moderador y si no es el mismo usuario de la consulta
        if usuario.rol == 'moderador' and session['id_usuario'] != usuario.id_usuario:
            # Redirige a la ruta de la biblioteca general
            return redirect(url_for('biblioteca.biblioteca'))
        # Consulta para obtener todos los archivos aprobados subidos por el usuario específico
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario, estado="aprobado").all()
        # Renderiza la plantilla 'shared_files.html' pasando los archivos y el nombre completo del usuario como contexto
        return render_template('shared_files.html', archivos=archivos, nombre_completo=usuario.nombre_completo)
    else:
        # Si no hay usuario en sesión, redirige a la página de inicio de sesión
        return redirect(url_for('auth.home'))
