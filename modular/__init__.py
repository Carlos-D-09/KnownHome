import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .database import db
from . import auth
from . import user
from . import api_user
from . import maestro
from . import alumno
from . import grupo
from . import grupo_alumno
from . import imagenes_maestro
from . import imagenes_alumno
from .database.Seeders.seed import configure_seed

from .database.Modelos.usuarios import Users
from .database.Modelos.codigos_verificacion import Codigos_verificacion
from .database.Modelos.objetos import Objetos
from .database.Modelos.imagenes_escaneadas import Imagenes_escaneadas
from .database.Modelos.passwords_antiguas import Passwords_antiguas
from .database.Modelos.maestros import Maestros
from .database.Modelos.alumnos import Alumnos
from .database.Modelos.grupos import Grupos
from .database.Modelos.grupo_alumno import Grupo_alumno
from .database.Modelos.incidencia import Incidencia

import tensorflow as tf
from keras.models import load_model

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins='*', resources= "/*")

    app.register_blueprint(auth.auth)
    app.register_blueprint(user.user)
    app.register_blueprint(api_user.api_user)
    app.register_blueprint(maestro.maestro)
    app.register_blueprint(alumno.alumno)
    app.register_blueprint(grupo.grupo)
    app.register_blueprint(grupo_alumno.grupo_alumno)
    app.register_blueprint(imagenes_maestro.imagenes_maestro)
    app.register_blueprint(imagenes_alumno.imagenes_alumno)

    load_dotenv()
    
    app.config.from_mapping(
        APP_EMAIL = os.environ.get('APP_EMAIL') ,
        APP_EMAIL_PASSWORD = os.environ.get('APP_EMAIL_PASSWORD'),
        SECRET_KEY = os.environ.get('SECRET_KEY'), #SALT
        SGBD = os.environ.get('SGBD'),
        DATABASE_HOST =os.environ.get('DATABASE_HOST'),
        DATABASE_USER =os.environ.get('DATABASE_USER'),
        DATABASE_PASSWORD =os.environ.get('DATABASE_PASSWORD'),
        DATABASE_PORT =os.environ.get('DATABASE_PORT'),
        DATABASE =os.environ.get('DATABASE'),
        OBJETOS = [
            'Abrelata', 'Alfiler', 'Anillo', 'Bateria', 'Boligrafo', 'Candado',
            'Cargador', 'Clavo', 'Cuchara', 'Cuchillo', 'Desarmador', 'Disco', 'Encendedor', 
            'Escaleras', 'Flauta', 'Globo', 'Jarra', 'Lentes', 'Licuadora', 'Linterna', 
            'Llave', 'Martillo', 'Navaja', 'Pelota', 'Rodillo', 'Silla', 'Taza', 'Tenedor', 'Vaso', 'Zapato' 
        ],
        # MODEL = load_model(os.environ.get('MODEL'))
    )

    db.configure_database(app)
    configure_seed(app)

    return app