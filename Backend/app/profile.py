from flask import Blueprint, render_template, session, redirect, url_for
from .models import Usuarios, Archivos

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil')
def perfil():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        usuario = Usuarios.query.get(id_usuario)
        archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
        return render_template('PerfilWebv3.html', usuario=usuario, archivos=archivos)
    else:
        return redirect(url_for('auth.home'))
