# Solemne2
Thyare Ibacache - Ignacia Moya

Informaticos:

Margarita Osorio - La Hechicera de la Nube

Marcos Valderrama - El Artífice del Rendimiento

Pablo Lores - El Guardián del Repositorio

instalaciones 
pip install Flask 
pip install Flask-SQLAlchemy 
pip install Flask-Uploads  
pip install Flask-OAuthlib Whoosh

BD.txt es el script para iniciar la base de datos 

## Base de datos
Primero es necesario tener el archivo .env en la carpeta Backend.

Para ejecutar la base de datos se debe correr en la carpeta "Backend" el comando:
```
docker compose up
```

Luego para conectarse a la base de datos se debe poner:
```
docker exec -it postgres_container psql -h localhost -U postgres -d udp_apuntes_en_linea
```


esta actualizacion es solo una pequeña base 



