# Solemne2

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



