from flask_sqlalchemy import SQLAlchemy
from config import Config  # Corregir la importación

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(256))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
