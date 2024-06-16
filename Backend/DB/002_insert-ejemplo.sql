-- Insert Ejemplo
INSERT INTO Usuarios (
    correo,
    contraseña,
    rol,
    nombre_completo,
    nombre_usuario,
    biografia,
    año_en_curso
) VALUES (
    'sofia.martinez@mail.udp.cl',
    '12345',
    'estudiante',
    'Sofía Andrea Martínez Díaz',
    'Sofía Andrea Martínez Díaz',
    'Me gusta estudiar con mi grupo de amigas en la facultad, mi ramo preferido es Psicología social.',
    '2do año'
);

INSERT INTO Usuarios (
    correo,
    contraseña,
    rol,
    nombre_completo,
    nombre_usuario,
    biografia,
    año_en_curso
) VALUES (
    'sandra.perez@mail.udp.cl',
    '12345',
    'estudiante',
    'Sandra Pérez',
    'Sandra Pérez',
    'Mi ramo menos preferido es Psicología social.',
    '2do año'
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