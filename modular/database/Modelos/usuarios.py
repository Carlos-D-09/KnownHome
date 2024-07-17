from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import string
import re

from ..db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemyseeder import ResolvingSeeder
from sqlalchemy import func, or_, and_, select

from .passwords_antiguas import Passwords_antiguas
from .codigos_verificacion import Codigos_verificacion
from .maestros import Maestros
from .alumnos import Alumnos
from .grupos import Grupos

class Users (db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    correo = db.Column(db.NVARCHAR(150), unique = True)
    password = db.Column(db.NVARCHAR(256))
    username = db.Column(db.NVARCHAR(50), unique = True)
    rol = db.Column(db.NVARCHAR(50))
    verified = db.Column(db.Boolean, default = False)
    active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, correo, password, username, rol, verified=False):
        self.correo = correo 
        self.password = self.generate_password(password)
        self.username = username
        self.rol = rol
        self.verified = verified

    def check_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        return check_password_hash(self.password, pwd)
    
    def check_old_passwords(self, pwd):
        passwords = Passwords_antiguas.get_by_user(self.id)
        passwords_list = [pwd._asdict() for pwd in passwords]
        pwd_secret_key = pwd + current_app.config['SECRET_KEY']
        for pwd in passwords_list:
            if check_password_hash(pwd['password_antigua'], pwd_secret_key):
                return True
        
        return False
    
    def set_new_username(self, username):
        self.username = username
        self.save()

        return True

    def set_new_email(self, new_email):
        codigo_verificacion = Codigos_verificacion.get_by_id(self.id)
        result, message, codigo = Codigos_verificacion.send_verification_email(self.username, new_email)
        if result:
            codigo_verificacion.correo = new_email
            codigo_verificacion.codigo = codigo
            codigo_verificacion.fecha_creacion = datetime.utcnow()
            codigo_verificacion.used = False
            codigo_verificacion.save()
            self.correo = new_email
            self.verified = False
            self.save()
            return True, None
        else:
            return False, message
        
    def set_new_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        self.password = generate_password_hash(pwd, method="pbkdf2")
        self.save()
        
    
    #Return false'La contraseña debe contener una letra mayúscula, una minúscula, un número y un símbolo'
    def validate_new_username(self, new_username):
        if self.username == new_username:
            return False, 'Realiza algún cambio'
        
        if not new_username: 
            return False, 'El nombre de usuario no puede estar vacío'
        
        if len(new_username) > 50:
            return False, 'El nombre de usuario no puede ser mayor a 50 caracteres'
        
        if Users.get_by_username(new_username):
            return False, 'Nombre de usuario en uso, porfavor introduce otro'
        
        return True, None

    #Return false if the email isn't valid, in case it is, returns true
    def validate_new_email(self, new_email):
        if self.correo == new_email:
            return False, 'Realiza algún cambio'
        
        if not new_email:
            return False, 'El correo electrónico no puede estar vacío' 
        
        if not Users.validate_email_format(new_email):
            return False, 'Formato de correo electrónico invalido'
        
        if Users.get_by_email(new_email):
            return False, 'Correo en uso, porfavor escoge otro'
        
        return True, None
    
    #Return false if the password isn't valid, in case it is, returns true
    def validate_new_password(self, password, new_password):
        
        if not self.check_password(password) or password == '':
            return False, 'Contraseña actual incorrecta'
        
        if not new_password:
            return False, 'La nueva contraseña no puede ser vacía'
        
        if len(new_password) < 8:
            return False, 'La contraseña no puede ser menor a 8 caracteres'
        
        if self.check_password(new_password):
            return False, 'Realiza algún cambio a tu contraseña'

        if not Users.validate_password_format(new_password):
            return False, 'La contraseña debe contener al menos un número, una letra mayúscula, minúscula y un símbolo'
        
        if self.check_old_passwords(new_password):
            return False, 'No puedes utilizar contraseñas antiguas'
        
        return True, None
    
    #Return all the administrator users
    def get_admin_users(self):
        return Users.query.filter_by(rol='administrador',active=True).with_entities(
                Users.id, 
                Users.username, 
                Users.correo, 
                func.date_format(Users.created_at, "%d/%m/%Y").label('created_at'),
                Users.verified
            ).all()

    #Return all the teachers users registered by the user
    def get_user_teachers(self):
        return Maestros.query.filter_by(registered_by=self.id, activo=True).with_entities(
            Maestros.id, 
            Maestros.username,
            func.date_format(Maestros.created_at, "%d/%m/%Y").label('created_at'),
            select(func.count()).select_from(Alumnos).filter(Alumnos.registered_by == Maestros.id, Alumnos.activo == True).label('alumnos_registrados'),
            select(func.count()).select_from(Grupos).filter(Grupos.id_maestro == Maestros.id).label('grupos_creados')
        ).all()
    
    #Search teacher by username register by the user
    def search_teacher_username(self, search_term):
        return Maestros.query.with_entities(
            Maestros.id,
            Maestros.username,
            func.date_format(Maestros.created_at, "%d/%m/%Y").label('created_at'),
            select(func.count()).select_from(Alumnos).filter(Alumnos.registered_by == Maestros.id, Alumnos.activo == True).label('alumnos_registrados'),
            select(func.count()).select_from(Grupos).filter(Grupos.id_maestro == Maestros.id).label('grupos_creados')            
        ).filter(
            and_(Maestros.username.ilike(f'%{search_term}%'), Maestros.activo == True, Maestros.registered_by == self.id)
        ).all()

    #Return true if the group belongs to any of the techers registered by the current user. In other case return False
    def validate_group(self, group_id):
        teachers = self.get_user_teachers()
        grupo = Grupos.get_by_id(group_id)
        for teacher in teachers:
            if teacher.id == grupo.id_maestro:
                return True
        
        return False

    def desactivate(self):
        self.active = False
        self.save()

    #Asocia la clase User a la tabla user de la base de datos
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def seed():
        file = "../Seeder/user.json"
        seeder = ResolvingSeeder(db.session())
        new_entities = seeder.load_entities_from_json_file(file)
        db.session.commit()

    
    @staticmethod
    def generate_password(password):
        pwd = password + current_app.config['SECRET_KEY']
        return generate_password_hash(pwd, method="pbkdf2")
    
    @staticmethod
    def validate_rol(rol):
        ROLES = (
            "supervisor",
            "administrador"
        )
        if rol.lower() not in ROLES:
            return False
        
        return True
        
    @staticmethod
    def validate_email_format(correo):
        correo_valido = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(correo_valido, correo) is not None
    
    @staticmethod
    def validate_password_format(pwd):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation

        lower = any(char in lowercase for char in pwd)
        upper = any(char in uppercase for char in pwd)
        digit = any(char in digits for char in pwd)
        symbol = any(char in symbols for char in pwd)
        
        if lower and upper and digit and symbol:
            return True
        else:
            return False
    
    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)
    
    @staticmethod
    def get_general_info(id):
        return Users.query.filter_by(id=id).with_entities(Users.id, Users.username, Users.correo, Users.rol).first()
    
    @staticmethod
    def get_general_info_admin(id_usuario):
        return Users.query.filter_by(id=id_usuario, rol='administrador', active=True).with_entities(Users.id, Users.username, Users.correo, Users.rol).first()
    
    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(correo=email).first()
    
    @staticmethod
    def get_by_username(username):
        return Users.query.filter_by(username=username).first()
    
    @staticmethod 
    def get_authentified(id):
        return Users.query.filter_by(id==id, verified=True)

    #Search admin user by username and email
    @staticmethod
    def search_admin_user(search_term):
        return Users.query.with_entities(
            Users.id,
            Users.username,
            Users.correo,
            func.date_format(Users.created_at, "%d/%m/%Y").label('created_at'),
            Users.verified
        ).filter(
            or_(
                and_(Users.correo.ilike(f'%{search_term}%'), Users.rol == 'administrador', Users.active == True),
                and_(Users.username.ilike(f'%{search_term}%'), Users.rol == 'administrador', Users.active == True)
            )
        ).all()