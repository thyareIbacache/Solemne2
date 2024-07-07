from flask import Blueprint, render_template, request, jsonify
from .models import Archivos, db

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/api/archivos', methods=['GET'])
def get_archivos():
    archivos = Archivos.query.filter_by(estado='pendiente').all()
    archivos_list = [{
        'id': archivo.id_archivo,
        'nombre': archivo.nombre_archivo,
        'usuario': archivo.usuario_que_lo_subio,
        'fecha_carga': archivo.fecha_subida.strftime("%Y-%m-%d %H:%M:%S")
    } for archivo in archivos]
    return jsonify(archivos_list)

@auditoria_bp.route('/api/archivos/<int:id>/aprobar', methods=['POST'])
def aprobar_archivo(id):
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'aprobado'
        db.session.commit()
        return jsonify({'message': 'Archivo aprobado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

@auditoria_bp.route('/api/archivos/<int:id>/rechazar', methods=['POST'])
def rechazar_archivo(id):
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'rechazado'
        archivo.auditado = False  # Asegurar que no esté auditado
        db.session.commit()
        return jsonify({'message': 'Archivo rechazado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

@auditoria_bp.route('/auditoria', methods=['GET'])
def auditoria():
    return render_template('admin/auditoria.html')
