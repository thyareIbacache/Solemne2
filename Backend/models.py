from flask_sqlalchemy import SQLAlchemy
from config import Config  # Corregir la importación

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    rol = db.Column(db.String(50), nullable=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(256))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
