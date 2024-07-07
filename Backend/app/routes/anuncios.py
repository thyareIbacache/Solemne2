from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Usuarios, db 

anuncios_bp = Blueprint('anuncios', __name__)

@anuncios_bp.route('/anuncios')
def anuncios():
    return render_template('anuncios.html')