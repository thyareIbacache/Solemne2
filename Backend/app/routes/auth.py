from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Usuarios
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint('auth', __name__)

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
            return redirect(url_for('profile.perfil'))
        else:
            mensaje = 'Credenciales inválidas'
            return render_template('Login.html', error_message=mensaje, username=correo)
    
    error_message = request.args.get('error', None)
    if error_message:
        return render_template('Login.html', error_message=error_message)

    return render_template('Login.html')

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
    return f"{user_info}"

@auth_bp.route('/logout')
def logout():
    session.pop('id_usuario', None)
    return redirect(url_for('auth.home'))

