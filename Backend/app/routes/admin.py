from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .models import Usuarios, db
from datetime import datetime
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuarios.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios', methods=['POST'])
def add_usuario():
    nombre_completo = request.form['nombre_completo']
    correo = request.form['correo']
    rol = request.form['rol']
    nuevo_usuario = Usuarios(
        nombre_completo=nombre_completo,
        correo=correo,
        rol=rol,
        contraseña=generate_password_hash('defaultpassword'),  # Set a default password, user should change it later
        nombre_usuario='',
        biografia='',
        año_ingreso=datetime.now().year
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for('admin.get_usuarios'))
