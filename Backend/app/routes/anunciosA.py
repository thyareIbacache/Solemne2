import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .models import Anuncio, db

anunciosA_bp = Blueprint('anunciosA', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@anunciosA_bp.route('/anunciosA')
def anunciosA():
    anuncios = Anuncio.query.all()
    return render_template('admin/anunciosA.html', anuncios=anuncios)

@anunciosA_bp.route('/anunciosA/nuevo', methods=['GET', 'POST'])
def nuevo_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        cuerpo = request.form['cuerpo']
        imagen = request.files['imagen']

        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
        else:
            imagen_path = None

        nuevo_anuncio = Anuncio(titulo=titulo, cuerpo=cuerpo, imagen=imagen_path)
        db.session.add(nuevo_anuncio)
        db.session.commit()

        flash('Anuncio creado exitosamente!', 'success')
        return redirect(url_for('anunciosA.anunciosA'))
    
    return render_template('admin/nuevo_anuncio.html')