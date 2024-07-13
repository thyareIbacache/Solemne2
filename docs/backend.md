# Backend "UDP Apuntes en Línea - Facultad de Psicología"
## Descripción General
El backend de "UDP Apuntes en Línea" es responsable de gestionar la lógica del servidor, la interacción con la base de datos, la autenticación de usuarios y la administración de archivos. Está diseñado para ser seguro, eficiente y escalable, proporcionando las funcionalidades necesarias para que el frontend pueda operar correctamente.

**Tecnologías Utilizadas:**
- **Lenguaje de programación:** Python.
- **Framework:** Flask.
- **Base de Datos:** PostgreSQL.
- **Almacenamiento de Archivos:** Azure Storage.

## Requisitos y Dependencias
### Archivo requirements.txt
```
Flask==2.3.2
Flask-SQLAlchemy==2.5.1
Flask-Uploads==0.2.1
Flask-OAuthlib==0.9.6
Whoosh==2.7.4
cryptography==41.0.1
psycopg2-binary==2.9.6
python-dotenv==0.19.2
SQLAlchemy==1.4.29
Authlib==1.3.1

```
### Instalación de dependencias
```
pip install -r requirements.txt
```

## Modelo de Base de Datos
### Definición de tablas
```
CREATE TABLE Usuarios (
    id_usuario SERIAL PRIMARY KEY,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rol VARCHAR(50) CHECK (rol IN ('estudiante', 'moderador')) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    nombre_usuario VARCHAR(255) NOT NULL,
    biografia VARCHAR(1000) NOT NULL,
    año_ingreso INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE),
    google_id VARCHAR(255) UNIQUE,
    google_image_url VARCHAR(500),
    refresh_token VARCHAR(255)
);

CREATE TABLE Cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre_curso VARCHAR(255) NOT NULL,
    facultad VARCHAR(255) NOT NULL,
    semestre VARCHAR(50) NOT NULL
);

CREATE TABLE Cursos_Usuarios (
    id_usuario INTEGER REFERENCES Usuarios(id_usuario),
    id_curso INTEGER REFERENCES Cursos(id_curso),
    PRIMARY KEY (id_usuario, id_curso)
);

CREATE TABLE Archivos (
    id_archivo SERIAL PRIMARY KEY,
    id_curso INTEGER REFERENCES Cursos(id_curso),
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    asignatura VARCHAR(255) NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_que_lo_subio INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    etiquetas VARCHAR(255), -- JSON o lista separada por comas
    ruta_archivo VARCHAR(255) NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'aprobado', 'rechazado')) DEFAULT 'pendiente',
    comentarios_rechazo VARCHAR(255),
    unidad VARCHAR(10),
    auditado BOOLEAN DEFAULT FALSE
);

CREATE TABLE Archivos_Cursos (
    id_curso INTEGER REFERENCES Cursos(id_curso),
    id_archivo INTEGER REFERENCES Archivos(id_archivo),
    PRIMARY KEY (id_curso, id_archivo)
);

CREATE TABLE Notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    mensaje VARCHAR(255) NOT NULL,
    fecha_notificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE
);

CREATE TABLE Logs (
    id_log SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    accion VARCHAR(255) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Anuncios (
    id_anuncio SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    cuerpo VARCHAR(255) NOT NULL,
    imagen VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuarios_correo ON Usuarios(correo);
CREATE INDEX idx_archivos_nombre ON Archivos(nombre_archivo);
CREATE INDEX idx_archivos_fecha_subida ON Archivos(fecha_subida);
CREATE INDEX idx_notificaciones_fecha ON Notificaciones(fecha_notificacion);
CREATE INDEX idx_logs_fecha ON Logs(fecha);

```
## Autenticación y Autorización
### OAuth con Google
**Flujo de Trabajo**
1. El usuario inicia sesión utilizando su cuenta de Google.
2. La aplicación redirige a Google para la autenticación.
3. Google devuelve un token de acceso.
4. La aplicación utiliza el token para obtener información del usuario y crear una sesión.

### Roles de Usuario
- **Estudiantes:** Pueden subir y descargar archivos, ver anuncios y editar su información.
- **Moderadores:** Pueden revisar, aprobar o rechazar archivos.

## Gestión de Archivos
### Subida de Archivos
**Proceso:**
1. El usuario selecciona un archivo y completa el formulario de subida.
2. El frontend envía una solicitud POST al backend con los datos y el archivo.
3. El backend guarda el archivo en Azure Storage y almacena los metadatos en la base de datos.

### Descarga de Archivos
**Proceso:**
1. El usuario selecciona un archivo aprobado para descargar.
2. El frontend envía una solicitud GET al backend.
3. El backend obtiene el archivo desde Azure Storage y lo envía al frontend para su descarga
