# UDP Apuntes en Línea
"UDP Apuntes en Línea - Facultad de Psicología" es un sitio web colaborativo diseñado para los estudiantes de la Universidad Diego Portales en la facultad de Psicología. Su objetivo es facilitar el acceso y poder compartir material complementario de estudio entre los estudiantes. El sitio permite a los usuarios ingresar utilizando su correo y clave UDP, mediante Google o ingresándolo directamente. Al iniciar sesión, pueden acceder a apuntes y recursos de estudios categorizados por cursos de interés o que se encuentren cursando actualmente. 

Los tipos de documentos que se pueden compartir incluyen "Apuntes de cátedra", "Guías de Ejercicios", "Controles", "Tareas", "Solemnes" y "Exámenes". 

Las coordinaciones de carrera actúan como moderadores para asegurar la calidad y pertinencia del material compartido.

## Arquitectura del Sistema
El sistema sigue una arquitectura repositorio con la infraestructura de la nube de Azure, contando de un frontend interactivo y un backend que cumple los requerimientos del sistema.

### Diagrama de Arquitectura
El diagrama de Arquitectura es el siguiente:

![Arquitectura_sistema](https://github.com/user-attachments/assets/b183e393-2000-4755-ac70-37a06b775b8d)

## Componentes del Sistema
### Interfaz usuario
- La interfaz de usuario permite a los estudiantes y moderadores interactuar con el sistema, accediendo a sus respectivas funcionalidades. 
- **Tecnologías Utilizadas:** HTML, Tailwind CSS, JavaScript.
- **Funcionalidades clave:** Autenticación de usuarios, incorporación de cursos, navegación por categorías, subida y descarga de documentos, generación de anuncios, validación o rechazo de documentos, búsqueda de perfiles.

### Backend
1. API?
2. Autenticación
3. Almacenamiento
4. Base de Datos
5. Moderación?

## Interacción entre Componentes
El siguiente diagrama presenta la interacción entre los componentes del sistema:
```
Aquí va el diagrama

```
## Metodología de uso

Antes de ejecutar, es necesario agregar un archivo .env en la carpeta 'Backend', esta debe contener:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
DBPORT=
PORT=
SECRET_KEY=
DATABASE_URL=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_METADATA_URL=
```

## Ejecutar

Para ejecutar la base de datos y la app de flask se debe correr en la carpeta 'Backend' el comando:
```
docker compose up
```

## Base de datos

Para conectarse a la base de datos se debe poner:
```
docker exec -it postgres_container psql -h localhost -U <POSTGRES_USER> -d udp_apuntes_en_linea
```
e ingresar la contraseña.

Para agregar un usuario al rol 'moderador':
```
docker exec -i postgres_container psql -h localhost -U <POSTGRES_USER> -d udp_apuntes_en_linea -c "UPDATE usuarios SET rol = 'moderador' WHERE id_usuario = <ID_USUARIO>;"
```

esta actualizacion es solo una pequeña base 



