import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') #or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #or 'sqlite:///udp_apuntes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # Tamaño máximo del archivo (en bytes) - 300 MB
    UPLOAD_FOLDER = './uploads/'
