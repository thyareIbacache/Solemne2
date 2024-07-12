import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .models import Anuncio, db

# Crea un Blueprint llamado 'anunciosA' para modularizar la aplicación.
anunciosA_bp = Blueprint('anunciosA', __name__)

# Define las extensiones de archivo permitidas para las imágenes.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida.

    Args:
        filename (str): El nombre del archivo a verificar.

    Returns:
        bool: True si el archivo tiene una extensión permitida, False en caso contrario.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@anunciosA_bp.route('/anunciosA')
def anunciosA():
    """
    Ruta para listar todos los anuncios.

    Returns:
        str: Renderiza el template 'admin/anunciosA.html' con todos los anuncios.
    """
    anuncios = Anuncio.query.all()
    return render_template('admin/anunciosA.html', anuncios=anuncios)

@anunciosA_bp.route('/anunciosA/nuevo', methods=['GET', 'POST'])
def nuevo_anuncio():
    """
    Ruta para crear un nuevo anuncio.

    Si la solicitud es GET, renderiza el formulario para crear un nuevo anuncio.
    Si la solicitud es POST, procesa los datos del formulario y crea el nuevo anuncio.

    Returns:
        str: Renderiza el template 'admin/nuevo_anuncio.html' o redirige a la lista de anuncios.
    """
    if request.method == 'POST':
        titulo = request.form['titulo']
        cuerpo = request.form['cuerpo']
        imagen = request.files['imagen']

        # Verifica si el archivo de imagen es permitido y guarda la imagen en el servidor.
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
        else:
            imagen_path = None

        # Crea un nuevo objeto Anuncio y lo guarda en la base de datos.
        nuevo_anuncio = Anuncio(titulo=titulo, cuerpo=cuerpo, imagen=imagen_path)
        db.session.add(nuevo_anuncio)
        db.session.commit()

        flash('Anuncio creado exitosamente!', 'success')
        return redirect(url_for('anunciosA.anunciosA'))
    
    return render_template('admin/nuevo_anuncio.html')
