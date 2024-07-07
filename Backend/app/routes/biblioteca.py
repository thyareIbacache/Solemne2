from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, db, Cursos
from datetime import datetime

biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/biblioteca')
def biblioteca():
    archivos = Archivos.query.all()
    return render_template('biblioteca.html', archivos=archivos)

@biblioteca_bp.route('/biblioteca-cursos/<int:id_curso>')
def biblioteca_cursos(id_curso):
    archivos = Archivos.query.filter_by(curso_id=id_curso).all()
    nombre_curso = Cursos.query.filter_by(id_curso=id_curso).first().nombre_curso
    return render_template('bibliocursos.html', archivos=archivos, nombre_curso=nombre_curso)

@biblioteca_bp.route('/shared')
def shared():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
        return render_template('shared_files.html', archivos=archivos)
    else:
        return redirect(url_for('auth.home'))