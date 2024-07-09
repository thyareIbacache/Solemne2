from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Anuncio, db

anunciosA_bp = Blueprint('anunciosA', __name__)

@anunciosA_bp.route('/anunciosA')
def anunciosA():
    anuncios = Anuncio.query.all()
    return render_template('admin/anunciosA.html', anuncios=anuncios)

@anunciosA_bp.route('/anunciosA/nuevo', methods=['GET', 'POST'])
def nuevo_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        cuerpo = request.form['cuerpo']
        imagen = request.form['imagen']

        nuevo_anuncio = Anuncio(titulo=titulo, cuerpo=cuerpo, imagen=imagen)
        db.session.add(nuevo_anuncio)
        db.session.commit()

        flash('Anuncio creado exitosamente!')
        return redirect(url_for('anunciosA.anunciosA'))
    
    return render_template('admin/nuevo_anuncio.html')
