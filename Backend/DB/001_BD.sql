-- Crear la base de datos
-- CREATE DATABASE udp_apuntes_en_linea;

-- Conectar a la base de datos
\c udp_apuntes_en_linea;

-- Crear la tabla Usuarios
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
    año_en_curso VARCHAR(50) NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    google_image_url VARCHAR(500)
);

-- Crear la tabla Cursos
CREATE TABLE Cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre_curso VARCHAR(255) NOT NULL,
    facultad VARCHAR(255) NOT NULL,
    semestre VARCHAR(50) NOT NULL
);

-- Crear la tabla Archivos
CREATE TABLE Archivos (
    id_archivo SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    asignatura VARCHAR(255) NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_que_lo_subio INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    etiquetas VARCHAR(255), -- JSON o lista separada por comas
    ruta_archivo VARCHAR(255) NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'aprobado', 'rechazado')) DEFAULT 'pendiente',
    comentarios_rechazo VARCHAR(255),
    unidad VARCHAR(10)
);

-- Crear la tabla intermedia Archivos_Cursos
CREATE TABLE Archivos_Cursos (
    id SERIAL PRIMARY KEY,
    id_archivo INT REFERENCES Archivos(id_archivo) ON DELETE CASCADE,
    id_curso INT REFERENCES Cursos(id_curso) ON DELETE CASCADE
);

-- Crear la tabla Notificaciones
CREATE TABLE Notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    mensaje VARCHAR(255) NOT NULL,
    fecha_notificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE
);

-- Crear la tabla Logs
CREATE TABLE Logs (
    id_log SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    accion VARCHAR(255) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices adicionales para optimización
CREATE INDEX idx_usuarios_correo ON Usuarios(correo);
CREATE INDEX idx_archivos_nombre ON Archivos(nombre_archivo);
CREATE INDEX idx_archivos_fecha_subida ON Archivos(fecha_subida);
CREATE INDEX idx_notificaciones_fecha ON Notificaciones(fecha_notificacion);
CREATE INDEX idx_logs_fecha ON Logs(fecha);
