from flask import Blueprint, redirect, url_for, session
from flask_oauthlib.client import OAuth

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key='GOOGLE_CLIENT_ID',
    consumer_secret='GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@auth_bp.route('/login')
def login():
    return google.authorize(callback=url_for('auth.authorized', _external=True))

@auth_bp.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('index'))

@auth_bp.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    # Process user information here (e.g., create user in DB)
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
