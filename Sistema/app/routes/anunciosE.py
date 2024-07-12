from flask import Blueprint, render_template
from .models import Anuncio

anunciosE_bp = Blueprint('anunciosE', __name__)

@anunciosE_bp.route('/anunciosE')
def anunciosE():
    # Obtener todos los anuncios de la base de datos
    anuncios = Anuncio.query.all()
    
    # Renderizar la plantilla con los anuncios
    return render_template('anunciosE.html', anuncios=anuncios)