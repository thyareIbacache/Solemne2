from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, db
from datetime import datetime

biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/biblioteca')
def biblioteca():
    archivos = Archivos.query.all()
    return render_template('biblioteca.html', archivos=archivos)

@biblioteca_bp.route('/biblioteca-cursos')
def biblioteca_cursos():
    archivos = Archivos.query.filter_by(curso='').all()
    return render_template('bibliocursos.html', archivos=archivos, nombre_curso='')

@biblioteca_bp.route('/shared')
def shared():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
        return render_template('shared_files.html', archivos=archivos)
    else:
        return redirect(url_for('auth.home'))