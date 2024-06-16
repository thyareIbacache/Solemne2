from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config  # Corregir la importación

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    rol = db.Column(db.String(50), nullable=False)
    nombre_completo = db.Column(db.String(255), nullable=False)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    año_ingreso = db.Column(db.Integer, nullable=False)
    año_en_curso = db.Column(db.String(50), nullable=False)


class Archivos(db.Model):
    __tablename__ = 'archivos'
    id_archivo = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    asignatura = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_que_lo_subio = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    etiquetas = db.Column(db.String(255))
    ruta_archivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')
    unidad = db.Column(db.String(10))
    comentarios_rechazo = db.Column(db.String(255))

    usuario = db.relationship('Usuarios', backref=db.backref('archivos', lazy=True))
