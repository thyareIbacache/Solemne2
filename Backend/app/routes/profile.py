from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Usuarios, Archivos, Cursos_Usuarios, Cursos, db
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil/', defaults={'id_usuario': None})
@profile_bp.route('/perfil', defaults={'id_usuario': None})
@profile_bp.route('/perfil-<int:id_usuario>')
def perfil(id_usuario):
    if 'id_usuario' in session:

        if id_usuario is None:
            id_usuario = session['id_usuario']
        usuario = Usuarios.query.get(id_usuario)

        if usuario.rol == 'moderador' and session['id_usuario'] != usuario.id_usuario:
            return redirect(url_for('biblioteca.biblioteca'))
    
        if usuario:
            archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario, estado="aprobado").limit(6).all()
            total_archivos = Archivos.query.filter_by(usuario_que_lo_subio=id_usuario, estado="aprobado").count()

            id_cursos = Cursos_Usuarios.query.filter_by(id_usuario=usuario.id_usuario).all()
            lista_id_cursos = [curso.id_curso for curso in id_cursos]
            cursos = Cursos.query.filter(Cursos.id_curso.in_(lista_id_cursos)).all()

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
            return render_template('perfil.html', usuario=usuario, cursos=cursos, archivos=archivos, total_archivos=total_archivos, año_cursando=texto)
        else:
            return redirect(url_for('auth.home'))
    else:
        return redirect(url_for('auth.home'))

@profile_bp.route('/update-perfil', methods=['GET', 'POST'])
def update_perfil():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nombre_completo = request.form.get('nombre_completo')
        nombre_usuario = request.form.get('nombre_usuario')
        biografia = request.form.get('biografia')
        año_ingreso = int(request.form.get('año_ingreso'))
        años_ingreso = [year for year in range(datetime.now().year, datetime.now().year - 21, -1)]

        cursos_inscritos = request.form.getlist('curso_inscrito')

        cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()
    
    if not nombre_completo or not nombre_usuario or not biografia or not año_ingreso:
        mensaje = 'Por favor, completa todos los campos del formulario.'
        return render_template('editarPerfil.html', error_message=mensaje, cursos=cursos, cursos_inscritos=cursos_inscritos, usuario=usuario, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, biografia=biografia)
    
    if not cursos_inscritos:
        mensaje = 'Debes seleccionar almenos un curso.'
        return render_template('editarPerfil.html', error_message=mensaje, cursos=cursos, cursos_inscritos=cursos_inscritos, usuario=usuario, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, biografia=biografia)

    if len(cursos_inscritos) > 6:
        mensaje = 'Puedes seleccionar maximo 6 cursos.'
        return render_template('editarPerfil.html', error_message=mensaje, cursos=cursos, cursos_inscritos=cursos_inscritos, usuario=usuario, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, biografia=biografia)

    id_usuario = session['id_usuario']
    usuario = Usuarios.query.get(id_usuario)

    usuario.nombre_usuario = nombre_usuario
    usuario.biografia = biografia
    usuario.año_ingreso = int(año_ingreso)

    Cursos_Usuarios.query.filter(Cursos_Usuarios.id_usuario == id_usuario).delete()
    db.session.commit()

    for curso in cursos_inscritos:
        inscripcion_curso = Cursos_Usuarios(
            id_usuario=id_usuario,
            id_curso=Cursos.query.filter_by(nombre_curso=curso).first().id_curso
        )
        db.session.add(inscripcion_curso)
    db.session.commit()

    return redirect(url_for('auth.home'))

@profile_bp.route('/update-clave', methods=['GET', 'POST'])
def update_clave():
    contraseña_actual = request.form.get('contraseña_actual')
    contraseña_nueva = request.form.get('contraseña')
    rep_contraseña_nueva = request.form.get('rep_contraseña')
    if not contraseña_actual or not contraseña_nueva or not rep_contraseña_nueva:
        mensaje = 'Por favor, completa todos los campos del formulario.'
        return render_template('editarPerfil.html', error_message=mensaje)
    
    if contraseña_nueva != rep_contraseña_nueva:
        mensaje = 'Por favor, las contraseñas nuevas deben coincidir.'
        return render_template('editarPerfil.html', error_message=mensaje)
    
    id_usuario = session['id_usuario']
    usuario = Usuarios.query.get(id_usuario)

    if contraseña_actual != usuario.contraseña:
        mensaje = 'Por favor, debes escribir tu contraseña actual correctamente.'
        return render_template('editarPerfil.html', error_message=mensaje)

    usuario.contraseña = contraseña_nueva
    db.session.commit()
    
    return redirect(url_for('auth.home'))

@profile_bp.route('/editar-perfil')
def editar_perfil():
    id_usuario = session['id_usuario']
    if id_usuario:
        usuario = Usuarios.query.get(id_usuario)
    else:
        return redirect(url_for('auth.home'))
    
    id_cursos = Cursos_Usuarios.query.filter_by(id_usuario=usuario.id_usuario).all()
    lista_id_cursos = [curso.id_curso for curso in id_cursos]
    cursos_inscritos = Cursos.query.with_entities(Cursos.nombre_curso).filter(Cursos.id_curso.in_(lista_id_cursos)).all()
    nombres_cursos = [curso[0] for curso in cursos_inscritos]

    cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()


    años_ingreso = [year for year in range(datetime.now().year, datetime.now().year - 21, -1)]
    return render_template('editarPerfil.html',
                            usuario=usuario, 
                            nombre_completo=usuario.nombre_completo,
                            nombre_usuario=usuario.nombre_usuario,
                            biografia=usuario.biografia,
                            año_ingreso=usuario.año_ingreso,
                            años_ingreso=años_ingreso,
                            cursos_inscritos=nombres_cursos,
                            cursos=cursos
                            ) 
