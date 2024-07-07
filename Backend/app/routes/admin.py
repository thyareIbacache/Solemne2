from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .models import Usuarios, db
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios', methods=['GET', 'POST'])
def get_usuarios():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        correo = request.form['correo']
        rol = request.form['rol']
        nuevo_usuario = Usuarios(
            nombre_completo=nombre_completo,
            correo=correo,
            rol=rol,
            contraseña=generate_password_hash('defaultpassword'),
            nombre_usuario='',
            biografia='',
            año_ingreso=datetime.now().year
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('admin.get_usuarios'))

    usuarios = Usuarios.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/admin-anuncios', methods=['GET', 'POST'])
def admin_anuncios():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        correo = request.form['correo']
        rol = request.form['rol']
        nuevo_usuario = Usuarios(
            nombre_completo=nombre_completo,
            correo=correo,
            rol=rol,
            contraseña=generate_password_hash('defaultpassword'),
            nombre_usuario='',
            biografia='',
            año_ingreso=datetime.now().year
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('admin.get_usuarios'))

    usuarios = Usuarios.query.all()
    return render_template('admin/anuncios.html', usuarios=usuarios)
