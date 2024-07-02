from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os

documents_bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'id_usuario' not in session:
        return jsonify({'error': 'User not logged in'})
    
    id_usuario = session['id_usuario']
    user_upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(id_usuario))
    os.makedirs(user_upload_folder, exist_ok=True)  # Crear carpeta si no existe

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_upload_folder, filename))  # Guardar en la carpeta del usuario
        # Save file info to database here
        return jsonify({'success': 'File successfully uploaded'})
    else:
        return jsonify({'error': 'Invalid file format'})
