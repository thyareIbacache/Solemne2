from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Usuarios, db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios', methods=['GET', 'POST'])
def get_usuarios():
    usuarios = Usuarios.query.all()
    return render_template('usuarios.html', usuarios=usuarios)