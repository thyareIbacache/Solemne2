# Arquitectura de "UDP Apuntes en Línea - Facultad de Psicología"
## Descripción General del Sistema
"UDP Apuntes en Línea - Facultad de Psicología" es una plataforma colaborativa para los estudiantes de la facultad de Psicología de la Universidad Diego Portales. Su objetivo es facilitar el intercambio de materiales complementarios de estudio, permitiendo que los estudiantes suban, accedan y descarguen apuntes, guías, solemnes y otros recursos académicos. Los documentos subidos son revisados y aprobados o rechazados por los coordinadores de carrera.

Los usuarios principales son:
-**Estudiantes:** Pueden subir y acceder a material de estudio.
-**Moderadores (Coordinadores de carrera):** Revisan y moderan el contenido subido.

## Diagrama de Arquitectura
El diagrama de arquitectura muestra la relación y comunicación entre los componentes del sistema:
![Arquitectura_sistema](https://github.com/user-attachments/assets/b183e393-2000-4755-ac70-37a06b775b8d)

## Componentes del sistema
### Frontend
1. Interfaz de usuario accesible desde un navegador web o móvil.
2. **Tecnologías utilizadas:** HTML, Tailwind CSS, JavaScript.
3. **Funcionalidades claves:** 
    - Registro e inicio de sesión.
    - Subida y descarga de documentos.
    - Navegación por cursos.
    - Visualización de notificaciones y anuncios.

### Backend
1. Gestión de lógica del sistema, autenticación e interacciones con la base de datos.
2. **Tecnologías utilizadas:** Python, Flask.
3. **Paquetes utilizados:** 
    - Flask==2.3.2
    - Flask-SQLAlchemy==2.5.1
    - Flask-Uploads==0.2.1
    - Flask-OAuthlib==0.9.6
    - Whoosh==2.7.4
    - cryptography==41.0.1
    - psycopg2-binary==2.9.6
    - python-dotenv==0.19.2
    - SQLAlchemy==1.4.29
    - Authlib==1.3.1

### Autenticación
1. Gestiona la autenticación de usuarios a través de OAuth con Google.
2. **Flujo de trabajo:** 
    - El usuario inicia sesión con su cuenta de Google: (@mail.udp.cl)
    - El servidor verifica las credenciales y genera un token.
    - El token se utiliza para acceder a recursos protegidos del sistema.

### Servidor de Almacenamiento
1. Maneja la subida, almacenamiento y descarga de documentos.
2. **Tecnologías utilizadas:** Azure Storage.
3. **Flujo de Trabajo:**
    - El usuario sube un documento a través de la interfaz de carga del sistema.
    - El servidor almacena el archivo en Azure Storage y guarda los metadatos en la base de datos.
    - El archivo queda pendiente de moderación.

### Moderación
1. Se gestiona la revisión y aprobación de documentos por parte de los moderadores.
2. **Flujo de Trabajo:**
    - El moderador revisa la lista de documentos pendientes.
    - El moderador aprueba o rechaza un documento.
    - El estado del documento se actualiza en la base de datos.

### Base de datos
1. Almacena la información de usuarios, cursos, documentos, notificaciones y logs.
2. **Tecnologías utilizadas:** PostgreSQL.

## Estructura de la Base de datos
### Tablas principales:
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
    refresh_token VARCHAR(255),
    estado VARCHAR(255)
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
## Flujo de Datos
### Inicio de Sesión
1. El usuario inicia sesión con su cuenta Google.
2. El servidor de autenticación verifica las credenciales y genera un token.
3. El usuario utiliza el token para acceder a recursos protegidos (interfaz usuario o moderador, carga y descarga de archivos, etc)

### Subida de documentos
1. El estudiante sube un documento a través de la interfaz de carga de archivos, especificando el título, curso y unidad.
2. El backend almacena el documento en Azure Storage y guarda los metadatos en la base de datos.
3. El documento se marca como "pendiente" y queda a la espera de revisión.

### Moderación de documentos
1. Un moderador revisa los documentos pendientes.
2. El moderador aprueba o rechaza el documento.
3. El estado del documento se actualiza en la base de datos y el estudiante puede visualizarlo en su perfil o en la interfaz de archivos compartidos/biblioteca de cursos.

