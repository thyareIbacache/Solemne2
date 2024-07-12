from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Usuarios, Cursos, Cursos_Usuarios, db 
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def format_name(name):
    return ' '.join(word.capitalize() for word in name.split())

@auth_bp.route('/', methods=['GET', 'POST'])
def home():
    if 'id_usuario' in session:
        return redirect(url_for('profile.perfil'))
    
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']
        usuario = Usuarios.query.filter_by(correo=correo).first()

        if usuario and (usuario.contraseña == contraseña):
            session['id_usuario'] = usuario.id_usuario
            if usuario.rol == 'moderador':
                return redirect(url_for('admin.get_usuarios'))
            return redirect(url_for('profile.perfil'))
        else:
            mensaje = 'Credenciales inválidas'
            return render_template('login.html', message=mensaje, msgType='alert' , username=correo)
    
    error_message = request.args.get('error', None)
    if error_message:
        return render_template('login.html', message=error_message, msgType='alert')

    return render_template('login.html')

@auth_bp.route('/login-google')
def login():
    oauth = current_app.oauth
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/callback')
def authorize():
    oauth = current_app.oauth
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        return f"{e}"

    resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
    user_info = resp.json()
    google_id = user_info['sub']
    usuario = Usuarios.query.filter_by(google_id=google_id).first()

    if usuario:
        session['id_usuario'] = usuario.id_usuario
        updated = False

        if usuario.google_image_url != user_info['picture']:
            usuario.google_image_url = user_info['picture']
            updated = True
        if token.get('refresh_token'):
            usuario.refresh_token = token.get('refresh_token')
            updated = True
        if updated:
            db.session.commit()
        return redirect(url_for('profile.perfil'))

    google_id_verifiq = Usuarios.query.filter_by(google_id=google_id).first()
    if google_id_verifiq is None:
        session['allow_register'] = user_info
        session['refresh_token'] = token.get('refresh_token')
        return redirect(url_for('auth.register'))
    else:
        return redirect(url_for('profile.perfil'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo')
        nombre_usuario = request.form.get('nombre_usuario')
        email = request.form.get('email')
        biografia = request.form.get('biografia')
        google_id = request.form.get('google_id')
        google_image_url = request.form.get('google_image_url')
        contraseña = request.form.get('contraseña')
        rep_contraseña = request.form.get('rep_contraseña')
        año_ingreso = int(request.form.get('año_ingreso'))
        años_ingreso = [year for year in range(datetime.now().year, datetime.now().year - 21, -1)]
        cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()
        cursos_inscritos = request.form.getlist('curso_inscrito')

        if not nombre_completo or not email or not biografia or not contraseña or not rep_contraseña or not año_ingreso or not nombre_usuario:
            mensaje = 'Por favor, completa todos los campos del formulario.'
            return render_template('register.html', message=mensaje, msgType='alert', cursos_inscritos=cursos_inscritos, cursos=cursos, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, email=email, biografia=biografia, google_id=google_id, google_image_url=google_image_url)
        
        if contraseña != rep_contraseña:
            mensaje = 'Las contraseñas deben coincidir.'
            return render_template('register.html', message=mensaje, msgType='alert', cursos_inscritos=cursos_inscritos, cursos=cursos, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, email=email, biografia=biografia, google_id=google_id, google_image_url=google_image_url)

        if not cursos_inscritos:
            mensaje = 'Debes seleccionar almenos un curso.'
            return render_template('register.html', message=mensaje, msgType='alert', cursos_inscritos=cursos_inscritos, cursos=cursos, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, email=email, biografia=biografia, google_id=google_id, google_image_url=google_image_url)

        if len(cursos_inscritos) > 6:
            mensaje = 'Puedes seleccionar maximo 6 cursos.'
            return render_template('register.html', message=mensaje, msgType='alert', cursos_inscritos=cursos_inscritos, cursos=cursos, año_ingreso=año_ingreso, años_ingreso=años_ingreso, nombre_completo=nombre_completo, nombre_usuario=nombre_usuario, email=email, biografia=biografia, google_id=google_id, google_image_url=google_image_url)


        nuevo_usuario = Usuarios(
            correo=email,
            contraseña=contraseña,
            rol='estudiante',
            nombre_completo=nombre_completo,
            nombre_usuario=nombre_usuario,
            año_ingreso=año_ingreso,
            biografia=biografia,
            google_id=google_id,
            google_image_url=google_image_url,
            refresh_token=session.get('refresh_token')
        )
        db.session.add(nuevo_usuario)

        db.session.commit()
        
        usuario = Usuarios.query.filter_by(google_id=google_id).first()
        id_usuario = usuario.id_usuario
        session['id_usuario'] = id_usuario

        for curso in cursos_inscritos:
            inscripcion_curso = Cursos_Usuarios(
                id_usuario=id_usuario,
                id_curso=Cursos.query.filter_by(nombre_curso=curso).first().id_curso
            )
            db.session.add(inscripcion_curso)
        db.session.commit()

        return redirect(url_for('profile.perfil'))

    if not session.get('allow_register'):
        return redirect(url_for('auth.home'))
     
    user_info = session.get('allow_register')
    nombre = format_name(user_info['given_name']).split()
    session.pop('allow_register')
    años_ingreso = [year for year in range(datetime.now().year, datetime.now().year - 21, -1)]
    cursos = Cursos.query.with_entities(Cursos.nombre_curso).all()
    return render_template('register.html', 
                            nombre_completo=format_name(user_info['name']),
                            nombre_usuario=nombre[0],
                            email=user_info['email'],
                            google_id=user_info['sub'],
                            google_image_url=user_info['picture'],
                            años_ingreso=años_ingreso,
                            cursos=cursos,
                            message='Debes registrarte antes de continuar.',
                            msgType='black'
                            ) 

@auth_bp.route('/logout')
def logout():
    session.pop('id_usuario', None)
    return redirect(url_for('auth.home'))

def refresh_google_token(user):
    oauth = current_app.oauth
    token = oauth.google.refresh_token(
        'https://accounts.google.com/o/oauth2/token',
        refresh_token=user.refresh_token
    )
    return token

# Prueba
@auth_bp.route('/test', methods=['GET'])
def test():
    return render_template('base.html')