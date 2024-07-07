from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory
from .models import Notificaciones, db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

notificacion_bp = Blueprint('notificacion', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@notificacion_bp.route('/notificaciones', methods=['GET'])
def get_notificaciones():
    notificaciones = Notificaciones.query.all()
    return render_template('notificaciones.html', notificaciones=notificaciones)

@notificacion_bp.route('/notificaciones', methods=['POST'])
def add_notificacion():
    titulo = request.form['titulo']
    texto = request.form['texto']
    file = request.files['file']
    filename = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    nueva_notificacion = Notificaciones(
        titulo=titulo,
        texto=texto,
        foto=filename,
        fecha=datetime.now()
    )
    db.session.add(nueva_notificacion)
    db.session.commit()

    return redirect(url_for('notificacion.get_notificaciones'))

@notificacion_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
