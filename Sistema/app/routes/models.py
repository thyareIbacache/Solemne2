from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()

# Modelo para la tabla 'usuarios'
class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)  # Identificador único del usuario
    correo = db.Column(db.String(255), unique=True, nullable=False)  # Correo electrónico del usuario
    contraseña = db.Column(db.String(255), nullable=False)  # Contraseña del usuario (almacenada como hash)
    fecha_registro = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # Fecha de registro del usuario
    rol = db.Column(db.String(50), nullable=False)  # Rol del usuario (por ejemplo, estudiante, profesor)
    nombre_completo = db.Column(db.String(255), nullable=False)  # Nombre completo del usuario
    nombre_usuario = db.Column(db.String(255), nullable=False)  # Nombre de usuario (único)
    biografia = db.Column(db.Text, nullable=False)  # Biografía del usuario
    año_ingreso = db.Column(db.Integer, nullable=False)  # Año de ingreso a la universidad
    google_id = db.Column(db.String(255), unique=True, nullable=True)  # ID de Google para integración SSO
    google_image_url = db.Column(db.String(500), nullable=True)  # URL de la imagen de perfil de Google
    refresh_token = db.Column(db.String(255), nullable=True)  # Token de actualización para integración SSO
    estado = db.Column(db.String(255), nullable=True) # Estado de la cuenta Bloqueado/Activo

# Modelo para la tabla 'cursos'
class Cursos(db.Model):
    __tablename__ = 'cursos'
    id_curso = db.Column(db.Integer, primary_key=True)  # Identificador único del curso
    nombre_curso = db.Column(db.String(255), nullable=False)  # Nombre del curso
    facultad = db.Column(db.String(255), nullable=False)  # Facultad a la que pertenece el curso
    semestre = db.Column(db.String(50), nullable=False)  # Semestre en el que se imparte el curso

# Tabla intermedia para la relación muchos a muchos entre Usuarios y Cursos
class Cursos_Usuarios(db.Model):
    __tablename__ = 'cursos_usuarios'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)  # FK a Usuarios
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), primary_key=True)  # FK a Cursos

# Modelo para la tabla 'archivos'
class Archivos(db.Model):
    __tablename__ = 'archivos'
    id_archivo = db.Column(db.Integer, primary_key=True)  # Identificador único del archivo
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=False)  # FK al curso relacionado
    nombre_archivo = db.Column(db.String(255), nullable=False)  # Nombre del archivo
    tipo = db.Column(db.String(50), nullable=False)  # Tipo de archivo (por ejemplo, pdf, docx)
    asignatura = db.Column(db.String(255), nullable=False)  # Asignatura a la que pertenece el archivo
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de subida del archivo
    usuario_que_lo_subio = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)  # FK al usuario que subió el archivo
    etiquetas = db.Column(db.String(255))  # Etiquetas para facilitar la búsqueda de archivos
    ruta_archivo = db.Column(db.String(255), nullable=False)  # Ruta donde se almacena el archivo
    estado = db.Column(db.String(50), default='pendiente')  # Estado del archivo (por ejemplo, pendiente, aprobado)
    unidad = db.Column(db.String(10))  # Unidad temática del archivo
    comentarios_rechazo = db.Column(db.String(255))  # Comentarios en caso de que el archivo sea rechazado

    # Relación con el modelo Usuarios
    usuario = db.relationship('Usuarios', backref=db.backref('archivos', lazy=True))

# Tabla intermedia para la relación muchos a muchos entre Archivos y Cursos
class Archivos_Cursos(db.Model):
    __tablename__ = 'archivos_cursos'
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), primary_key=True)  # FK a Cursos
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivos.id_archivo'), primary_key=True)  # FK a Archivos

# Modelo para la tabla 'anuncios'
class Anuncio(db.Model):
    __tablename__ = 'anuncios'
    id_anuncio = db.Column(db.Integer, primary_key=True)  # Identificador único del anuncio
    titulo = db.Column(db.String(255), nullable=False)  # Título del anuncio
    cuerpo = db.Column(db.Text, nullable=False)  # Contenido del anuncio
    imagen = db.Column(db.String(255), nullable=True)  # Ruta de la imagen asociada al anuncio
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación del anuncio
