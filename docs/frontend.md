# Frontend "UDP Apuntes en Linea - Facultad de Psicología"
## Descripción General
El frontend de "UDP Apuntes en Línea" es la interfaz de usuario accesible desde el navegador web. Está diseñado para proporcionar una experiencia intuitiva y fácil de usar, permitiendo a los estudiantes y moderadores interactuar con el sistema de manera eficiente.

**Tecnologías Utilizadas:**
- **HTML:** Para la estructura y el contenido de las páginas web.
- **Tailwind CSS:** Para el diseño y estilo visual de la interfaz de usuario.
- **JavaScript:** Para la interacción y funcionalidad dinámica del sitio web.

## Funcionalidades Principales
### Registro e Inicio de Sesión
- **Descripción:** Permite a los usuarios registrarse e iniciar sesión utilizando sus cuentas de Google (@mail.udp.cl).
- **Detalles de Implementación:** 
  - Uso de OAuth para la autenticación.
  - Interacción con el backend para verificar y almacenar credenciales.

### Subida de Documentos
- **Descripción:** Los estudiantes pueden subir documentos como apuntes, guías, tareas, etc.
- **Detalles de Implementación:** 
  - Formularios de subida con campos para nombre, tipo de documento, asignatura, unidad, etiquetas, y archivo.
  - Interacción con el backend para almacenar los documentos y metadatos.

### Navegación y Búsqueda de Documentos
- **Descripción:** Los usuarios pueden navegar y buscar documentos por curso, tipo, y etiquetas.
- **Detalles de Implementación:** 
  - Menús de navegación organizados por facultades, carreras y cursos.
  - Barra de búsqueda y filtros para facilitar la localización de documentos específicos.

### Moderación de Documentos
- **Descripción:** Los moderadores pueden revisar, aprobar o rechazar documentos subidos por los estudiantes.
- **Detalles de Implementación:** 
  - Panel de moderación con lista de documentos pendientes.
  - Formularios para aprobación/rechazo y comentarios de moderación.

### Notificaciones y Anuncios
- **Descripción:** Los usuarios reciben notificaciones sobre la aprobación/rechazo de sus documentos y anuncios importantes.
- **Detalles de Implementación:** 
  - Sistema de notificaciones según moderación.
  - Sección dedicada a anuncios y noticias relevantes.

## Diseño de la Interfaz

### Estilo Visual
- **Framework:** Tailwind CSS
- **Principios de Diseño:** 
  - Simplicidad y claridad.
  - Consistencia en el uso de colores, tipografía y espaciado.
  - Adaptabilidad a diferentes tamaños de pantalla (diseño responsivo).

### Componentes Principales
- **Header:** Incluye el logo, menú de navegación principal, y acceso a la cuenta del usuario.
- **Sidebar:** Menú lateral para navegación rápida por menú de navegación en vista móvil.
- **Main Content Area:** Área principal donde se muestra el contenido (documentos, formularios, notificaciones).
- **Footer:** Información adicional relacionada a la universidad.

## Interacción con el Backend

### API RESTful
- **Descripción:** El frontend interactúa con el backend a través de una API RESTful.
- **Detalles de Implementación:** 
  - Solicitudes HTTP (GET, POST, PUT, DELETE) para obtener y enviar datos.
  - Manejo de tokens de autenticación para proteger las solicitudes.

### Subida y Descarga de Documentos
- **Flujo de Trabajo:**
  1. El usuario selecciona un archivo y completa el formulario de subida.
  2. El frontend envía una solicitud POST al backend con los datos y el archivo.
  3. El backend almacena el archivo y responde con un mensaje de confirmación.
  4. El usuario puede descargar documentos aprobados a través de enlaces proporcionados en la interfaz.

### Manejo de Errores y Validación
- **Descripción:** El frontend incluye mecanismos para manejar errores y validar entradas de usuario.
- **Detalles de Implementación:** 
  - Mensajes de error claros y específicos.
  - Validación de formularios en el lado del usuario para asegurar la integridad de los datos.

## Seguridad

### Autenticación y Autorización
- **Descripción:** Uso de OAuth con Google para la autenticación de usuarios.
- **Detalles de Implementación:** 
  - Solicitud y verificación de tokens de acceso.
  - Control de acceso basado en roles (estudiantes y moderadores).

### Protección de Datos
- **Descripción:** Medidas para asegurar que los datos sensibles estén protegidos.
- **Detalles de Implementación:** 
  - Uso de HTTPS para todas las comunicaciones.
  - Almacenamiento seguro de tokens de autenticación.

