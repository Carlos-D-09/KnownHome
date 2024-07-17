import os

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from ..db import db
from .alumnos import Alumnos

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import func, select

from datetime import datetime
import string

class Maestros (db.Model):
    __tablename__ = 'maestros'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.NVARCHAR(50), unique = True)
    password = db.Column(db.NVARCHAR(256))
    activo = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    registered_by = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('maestro-usuario',lazy=True))

    def __init__(self, username, password, registered_by):
        self.username = username
        self.password = self.generate_password(password)
        self.registered_by = registered_by

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def create_directory(self):
        # Ruta del directorio a crear
        separador = os.path.sep
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        home_dir = separador.join(dir_actual.split(separador)[:-2])
        new_directory =  os.path.join(home_dir, f'static/images/maestros/{self.id}')

        # Verificar si el directorio no existe antes de crearlo
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

    def set_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        self.password = generate_password_hash(pwd, method="pbkdf2")

    def set_username(self, username):
        self.username = username
    
    def set_new_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        self.password = generate_password_hash(pwd, method="pbkdf2")
        self.save()

    def set_new_username(self, username):
        self.username = username
        self.save()
    
    def check_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        return check_password_hash(self.password, pwd)
    
    def verify_current_password(self, current_password):
        current_password_hashed = current_password + current_app.config['SECRET_KEY']
        return check_password_hash(self.password, current_password_hashed)

    def validate_new_username(self, new_username):
        if self.username == new_username:
            return False, 'Realiza algún cambio'
        
        if not new_username: 
            return False, 'El nombre de usuario no puede estar vacío'
        
        if len(new_username) > 50:
            return False, 'El nobmre de usuario no puede ser mayor a 50 caracteres'
        
        if Maestros.get_by_username(new_username):
            return False, 'Nombre de usuario en uso, porfavor introduce otro'
        
        return True, None

    def desactivate(self):
        self.activo = False
        self.save

    @staticmethod
    def get_general_info_teacher(id):
        return Maestros.query.filter_by(id=id).with_entities(Maestros.id, Maestros.username, Maestros.registered_by).first()

    @staticmethod
    def get_by_id(id):
        return Maestros.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return Maestros.query.filter_by(username=username, activo=True).first()
    
    @staticmethod
    def generate_password(password):
        pwd = password + current_app.config['SECRET_KEY']
        return generate_password_hash(pwd, method="pbkdf2")

    @staticmethod
    def validate_password_format(pwd):
        if len(pwd) < 8:
            return False, 'La contraseña tiene que ser almenos de 8 caracteres'
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation

        lower = any(char in lowercase for char in pwd)
        upper = any(char in uppercase for char in pwd)
        digit = any(char in digits for char in pwd)
        symbol = any(char in symbols for char in pwd)
        
        if lower and upper and digit and symbol:
            return True, None
        else:
            return False, 'La contraseña debe contener una letra mayúscula, una minúscula, un número y un símbolo'

    #Return the number of active teachers
    @staticmethod
    def get_active_number_teachers():
        return Maestros.query.filter_by(activo=True).count()
    
    @staticmethod
    def get_all():
        return Maestros.query.all()