# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY ./app/requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir --verbose -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Establece la variable de entorno para Flask
ENV FLASK_APP=run.py

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para correr la aplicación
CMD pip install --no-cache-dir -r requirements.txt && flask run --host=0.0.0.0
