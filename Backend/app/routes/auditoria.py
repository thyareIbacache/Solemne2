from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Usuarios, db
from datetime import datetime

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/auditoria', methods=['GET', 'POST'])
def usuarios():
    return render_template('auditoria.html')