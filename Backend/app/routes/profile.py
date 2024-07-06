from flask import Blueprint, render_template, session, redirect, url_for
from .models import Usuarios, Archivos
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil/', defaults={'id_usuario': None})
@profile_bp.route('/perfil', defaults={'id_usuario': None})
@profile_bp.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    if 'id_usuario' in session:

        if id_usuario is None:
            id_usuario = session['id_usuario']
        usuario = Usuarios.query.get(id_usuario)

        if usuario:
            archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario).all()
            current_year = datetime.now().year

            # Calcular los años pasados desde el año de ingreso del usuario
            years_passed = current_year - usuario.año_ingreso

            # Determinar el texto correspondiente
            if years_passed == 0:
                texto = "1er año"
            elif years_passed == 1:
                texto = "2do año"
            elif years_passed == 2:
                texto = "3er año"
            elif years_passed == 3:
                texto = "4to año"
            elif years_passed == 4:
                texto = "5to año"
            elif years_passed == 5:
                texto = "6to año"
            elif years_passed == 6:
                texto = "7mo año"
            elif years_passed == 7:
                texto = "8vo año"
            elif years_passed == 8:
                texto = "9no año"
            elif years_passed == 9:
                texto = "10mo año"
            else:
                texto = "Más de 10 años"
            return render_template('perfil.html', usuario=usuario, archivos=archivos, año_cursando=texto)
        else:
            return redirect(url_for('auth.home'))
    else:
        return redirect(url_for('auth.home'))

@profile_bp.route('/update-perfil')
def editar_perfil():
    return redirect(url_for('auth.home'))

@profile_bp.route('/update-clave')
def editar_perfil():
    return redirect(url_for('auth.home'))

@profile_bp.route('/editar-perfil')
def editar_perfil():
    id_usuario = session['id_usuario']
    if id_usuario:
        usuario = Usuarios.query.get(id_usuario)
    else:
        return redirect(url_for('auth.home'))

    años_ingreso = [year for year in range(datetime.now().year, datetime.now().year - 21, -1)]
    return render_template('editarPerfil.html', 
                            nombre_completo=usuario.nombre_completo,
                            nombre_usuario=usuario.nombre_usuario,
                            email=usuario.correo,
                            año_ingreso=usuario.año_ingreso,
                            años_ingreso=años_ingreso
                            ) 
