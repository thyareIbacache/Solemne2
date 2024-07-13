-- Insert Ejemplo
INSERT INTO Usuarios (
    correo,
    contraseña,
    rol,
    nombre_completo,
    nombre_usuario,
    biografia,
    google_id,
    google_image_url,
    estado
) VALUES (
    'sofia.martinez@mail.udp.cl',
    '12345',
    'estudiante',
    'Sofía Andrea Martínez Díaz',
    'Sofía Andrea Martínez Díaz',
    'Me gusta estudiar con mi grupo de amigas en la facultad, mi ramo preferido es Psicología social.',
    NULL,
    NULL,
    'Activo'
);

INSERT INTO Usuarios (
    correo,
    contraseña,
    rol,
    nombre_completo,
    nombre_usuario,
    biografia,
    google_id,
    google_image_url,
    estado
) VALUES (
    'sandra.perez@mail.udp.cl',
    '12345',
    'estudiante',
    'Sandra Pérez',
    'Sandra Pérez',
    'Mi ramo menos preferido es Psicología social.',
    NULL,
    NULL,
    'Activo'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Psicología de la Infancia',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Psicología de la Adole',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Psicología Comu II',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Investigación I',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo I',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo II',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo III',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo IV',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo V',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos (
    nombre_curso,
    facultad,
    semestre
) VALUES (
    'Curso Ejemplo VI',
    'Psicologia',
    '2024 - 1'
);

INSERT INTO Cursos_Usuarios (
    id_usuario,
    id_curso
) VALUES (
    1,
    1
);

INSERT INTO Cursos_Usuarios (
    id_usuario,
    id_curso
) VALUES (
    1,
    2
);

INSERT INTO Cursos_Usuarios (
    id_usuario,
    id_curso
) VALUES (
    1,
    3
);

INSERT INTO Cursos_Usuarios (
    id_usuario,
    id_curso
) VALUES (
    1,
    4
);
/* INSERT INTO Archivos (
        nombre_archivo, 
        tipo,
        asignatura, 
        usuario_que_lo_subio, 
        etiquetas, 
        ruta_archivo, 
        estado, 
        comentarios_rechazo,
        unidad
    ) VALUES (
        'documento.pdf', 
        'PDF',
        'Psicologia', 
        1, 
        'documento, 
        PDF', 
        '/archivos/documento.pdf', 
        'pendiente', 
        NULL,
        'I'
    );
*/