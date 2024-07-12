from flask import Blueprint, render_template, request, jsonify
from .models import Archivos, db

# Creación del Blueprint para la auditoría
auditoria_bp = Blueprint('auditoria', __name__)

# Ruta para obtener todos los archivos con estado 'pendiente'
@auditoria_bp.route('/api/archivos', methods=['GET'])
def get_archivos():
    """
    Retorna una lista de archivos con estado 'pendiente'.

    Endpoint:
        GET /api/archivos

    Retorno:
        JSON: Lista de archivos pendientes con los siguientes campos:
        - id: ID del archivo
        - nombre: Nombre del archivo
        - usuario: Usuario que subió el archivo
        - fecha_carga: Fecha y hora de subida del archivo en formato YYYY-MM-DD HH:MM:SS
    """
    archivos = Archivos.query.filter_by(estado='pendiente').all()
    archivos_list = [{
        'id': archivo.id_archivo,
        'nombre': archivo.nombre_archivo,
        'usuario': archivo.usuario_que_lo_subio,
        'ruta_archivo': archivo.ruta_archivo,
        'fecha_carga': archivo.fecha_subida.strftime("%Y-%m-%d %H:%M:%S")
    } for archivo in archivos]
    return jsonify(archivos_list)

# Ruta para aprobar un archivo específico
@auditoria_bp.route('/api/archivos/<int:id>/aprobar', methods=['POST'])
def aprobar_archivo(id):
    """
    Aprueba un archivo con el ID especificado.

    Endpoint:
        POST /api/archivos/<int:id>/aprobar

    Parámetros URL:
        id (int): ID del archivo a aprobar

    Retorno:
        JSON: Mensaje de éxito o error
        Código de estado HTTP:
            200: Archivo aprobado exitosamente
            404: Archivo no encontrado
    """
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'aprobado'
        db.session.commit()
        return jsonify({'message': 'Archivo aprobado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

# Ruta para rechazar un archivo específico
@auditoria_bp.route('/api/archivos/<int:id>/rechazar', methods=['POST'])
def rechazar_archivo(id):
    """
    Rechaza un archivo con el ID especificado.

    Endpoint:
        POST /api/archivos/<int:id>/rechazar

    Parámetros URL:
        id (int): ID del archivo a rechazar

    Retorno:
        JSON: Mensaje de éxito o error
        Código de estado HTTP:
            200: Archivo rechazado exitosamente
            404: Archivo no encontrado
    """
    archivo = Archivos.query.get(id)
    if archivo:
        archivo.estado = 'rechazado'
        archivo.auditado = False  # Asegurar que no esté auditado
        db.session.commit()
        return jsonify({'message': 'Archivo rechazado'}), 200
    return jsonify({'message': 'Archivo no encontrado'}), 404

# Ruta para renderizar la página de auditoría
@auditoria_bp.route('/auditoria', methods=['GET'])
def auditoria():
    """
    Renderiza la página de auditoría para administración.

    Endpoint:
        GET /auditoria

    Retorno:
        HTML: Página de auditoría
    """
    return render_template('admin/auditoria.html')
