from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .models import Usuarios, db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Definir un Blueprint llamado 'admin' para agrupar las rutas relacionadas con la administración
admin_bp = Blueprint('admin', __name__)

# Ruta para gestionar usuarios
@admin_bp.route('/usuarios', methods=['GET', 'POST'])
def get_usuarios():
    # Si el método de la solicitud es POST, se procesa el formulario para añadir un nuevo usuario
    if request.method == 'POST':
        # Recuperar datos del formulario
        nombre_completo = request.form['nombre_completo']
        correo = request.form['correo']
        clave = request.form['clave']
        rol = request.form['rol']
        
        # Crear un nuevo objeto Usuario con los datos del formulario y contraseñas por defecto hasheada
        nuevo_usuario = Usuarios(
            nombre_completo=nombre_completo,
            correo=correo,
            rol=rol,
            contraseña=clave,
            nombre_usuario='',
            biografia='',
            año_ingreso=datetime.now().year  # Asignar el año actual como año de ingreso
        )
        
        # Añadir el nuevo usuario a la sesión de la base de datos y confirmar la transacción
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Redirigir a la lista de usuarios después de añadir el nuevo usuario
        return redirect(url_for('admin.get_usuarios'))

    # Si el método de la solicitud es GET, recuperar todos los usuarios de la base de datos
    usuarios = Usuarios.query.all()
    
    # Renderizar la plantilla 'usuarios.html' con los datos de los usuarios
    return render_template('admin/usuarios.html', usuarios=usuarios)

# Ruta para gestionar anuncios
@admin_bp.route('/admin-anuncios', methods=['GET', 'POST'])
def admin_anuncios():
    # Si el método de la solicitud es POST, se procesa el formulario para añadir un nuevo anuncio
    if request.method == 'POST':
        # Recuperar datos del formulario
        nombre_completo = request.form['nombre_completo']
        correo = request.form['correo']
        rol = request.form['rol']
        
        # Crear un nuevo objeto Usuario con los datos del formulario y contraseñas por defecto hasheada
        nuevo_usuario = Usuarios(
            nombre_completo=nombre_completo,
            correo=correo,
            rol=rol,
            contraseña=generate_password_hash('defaultpassword'),  # Generar un hash de la contraseña por defecto
            nombre_usuario='',
            biografia='',
            año_ingreso=datetime.now().year  # Asignar el año actual como año de ingreso
        )
        
        # Añadir el nuevo usuario a la sesión de la base de datos y confirmar la transacción
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Redirigir a la lista de usuarios después de añadir el nuevo anuncio
        return redirect(url_for('admin.get_usuarios'))

    # Si el método de la solicitud es GET, recuperar todos los usuarios de la base de datos
    usuarios = Usuarios.query.all()
    
    # Renderizar la plantilla 'anuncios.html' con los datos de los usuarios
    return render_template('admin/anuncios.html', usuarios=usuarios)
