from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, db
from datetime import datetime

biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/biblioteca')
def biblioteca():
    archivos = Archivos.query.all()
    return render_template('biblioteca.html', archivos=archivos)