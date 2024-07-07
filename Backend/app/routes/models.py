from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    biografia = db.Column(db.Text, nullable=False)
    año_ingreso = db.Column(db.Integer, nullable=False)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    google_image_url = db.Column(db.String(500), nullable=True)
    refresh_token = db.Column(db.String(255), nullable=True)

class Cursos(db.Model):
    __tablename__ = 'cursos'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(255), nullable=False)
    facultad = db.Column(db.String(255), nullable=False)
    semestre = db.Column(db.String(50), nullable=False)

class Cursos_Usuarios(db.Model):
    __tablename__ = 'cursos_usuarios'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), primary_key=True)

class Archivos(db.Model):
    __tablename__ = 'archivos'
    id_archivo = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=False)
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
    auditado = db.Column(db.Boolean, default=False)  # Añadir la columna auditado

    usuario = db.relationship('Usuarios', backref=db.backref('archivos', lazy=True))

class Archivos_Cursos(db.Model):
    __tablename__ = 'archivos_cursos'
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), primary_key=True)
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivos.id_archivo'), primary_key=True)
