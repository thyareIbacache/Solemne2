from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, db, Cursos
from datetime import datetime

biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/biblioteca')
def biblioteca():
    archivos = Archivos.query.filter_by(estado="aprobado").all()
    cursos = Cursos.query.all()
    return render_template('biblioteca.html', archivos=archivos, cursos=cursos)

@biblioteca_bp.route('/biblioteca-cursos-<int:id_curso>')
def biblioteca_cursos(id_curso):
    archivos = Archivos.query.filter_by(id_curso=id_curso, estado="aprobado").all()
    nombre_curso = Cursos.query.filter_by(id_curso=id_curso).first().nombre_curso
    cursos = Cursos.query.all()
    return render_template('bibliocursos.html', archivos=archivos, nombre_curso=nombre_curso, cursos=cursos)


@biblioteca_bp.route('/shared')
@biblioteca_bp.route('/shared-<int:id_usuario>')
def shared(id_usuario):
    if 'id_usuario' in session:
        if id_usuario is None:
            id_usuario = session['id_usuario']
        usuario = Usuarios.query.filter_by(id_usuario=id_usuario).first()
        if usuario.rol == 'moderador' and session['id_usuario'] != usuario.id_usuario:
            return redirect(url_for('biblioteca.biblioteca'))
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario, estado="aprobado").all()
        return render_template('shared_files.html', archivos=archivos, nombre_completo=usuario.nombre_completo)
    else:
        return redirect(url_for('auth.home'))