from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import Archivos, Usuarios, db
from datetime import datetime

auditoria_bp = Blueprint('auditoria', __name__)

# Ruta para obtener la lista de archivos pendientes de revisión
@auditoria_bp.route('/api/archivos', methods=['GET', 'POST'])
def get_archivos():
    archivos = Archivos.query.filter_by(estado='pendiente').all()
    archivos_list = [{
        'id': archivo.id_archivo,
        'nombre': archivo.nombre_archivo,
        'usuario': Usuarios.query.get(archivo.usuario_que_lo_subio).nombre_completo,
        'fecha_carga': archivo.fecha_subida.strftime("%Y-%m-%d %H:%M:%S")
    } for archivo in archivos]
    return jsonify(archivos_list)

# Ruta para aprobar un archivo
@auditoria_bp.route('/api/archivos/<int:id>/aprobar', methods=['POST'])
def aprobar_archivo(id):
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'aprobado'
        db.session.commit()
        return jsonify({'message': 'Archivo aprobado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

# Ruta para rechazar un archivo
@auditoria_bp.route('/api/archivos/<int:id>/rechazar', methods=['POST'])
def rechazar_archivo(id):
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'rechazado'
        db.session.commit()
        return jsonify({'message': 'Archivo rechazado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

# Ruta para mostrar la página de auditoría
@auditoria_bp.route('/auditoria', methods=['GET'])
def auditoria():
    return render_template('auditoria.html')
