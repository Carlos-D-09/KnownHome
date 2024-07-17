import os
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from ..db import db
from sqlalchemy.dialects.mysql import INTEGER

from datetime import datetime
import string

class Alumnos (db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.NVARCHAR(50), unique = True)
    password = db.Column(db.NVARCHAR(256))
    activo = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    registered_by = db.Column(INTEGER(unsigned=True), db.ForeignKey('maestros.id'), nullable=False)
    maestro = db.relationship('Maestros', backref=db.backref('alumno-maestro',lazy=True))

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
        new_directory =  os.path.join(home_dir, f'static/images/alumnos/{self.id}')

        # Verificar si el directorio no existe antes de crearlo
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

    def set_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        self.password = generate_password_hash(pwd, method="pbkdf2")

    def check_password(self, password):
        pwd = password + current_app.config['SECRET_KEY']
        return check_password_hash(self.password, pwd)

    @staticmethod
    def get_by_id(id):
        return Alumnos.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return Alumnos.query.filter_by(username=username).first()
    
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
        
    @staticmethod
    def get_active_students_by_teacher(teacher_id):
        students = Alumnos.query.filter_by(registered_by=teacher_id, activo=True).all()
        students_list = []
        for student in students:
            student_dict = {
                'id': student.id,
                'username': student.username
            }
            students_list.append(student_dict)
        return students_list

    @staticmethod
    def get_inactive_students_by_teacher(teacher_id):
        students = Alumnos.query.filter_by(registered_by=teacher_id, activo=False).all()
        students_list = []
        for student in students:
            student_dict = {
                'id': student.id,
                'username': student.username
            }
            students_list.append(student_dict)
        return students_list

    @staticmethod
    def get_teacher_students(teacher_id):
        students = Alumnos.query.filter_by(registered_by=teacher_id).all()
        students_list = []
        for student in students:
            student_dict = {
                'id': student.id,
                'username': student.username,
                'activo': student.activo
            }
            students_list.append(student_dict)
        return students_list
    
    @staticmethod
    def search_students_registered_by_teacher(teacher_id, search_query):
        query = Alumnos.query.filter_by(registered_by=teacher_id, activo=True)
        if search_query:
            search = "%{}%".format(search_query)
            query = query.filter(Alumnos.username.ilike(search))
        students = query.all()
        
        students_list = []
        for student in students:
            student_dict = {
                'id': student.id,
                'username': student.username
            }
            students_list.append(student_dict)
        return students_list
    
    @staticmethod
    def search_deactivated_students_by_teacher(teacher_id, search_query):
        query = Alumnos.query.filter_by(registered_by=teacher_id, activo=False)
        if search_query:
            search = "%{}%".format(search_query)
            query = query.filter(Alumnos.username.ilike(search))
        students = query.all()
        
        students_list = []
        for student in students:
            student_dict = {
                'id': student.id,
                'username': student.username
            }
            students_list.append(student_dict)
        return students_list
    
    @staticmethod
    def deactivate_student(student_id, teacher_id):
        alumno = Alumnos.query.filter_by(id=student_id, registered_by=teacher_id).first()
        if not alumno:
            return None, 'No tienes permiso para dar de baja a este alumno o el alumno no existe.'

        if not alumno.activo:
            return None, 'El alumno ya ha sido dado de baja.'
        
        alumno.activo = False
        db.session.commit()
        return alumno, None
    
    @staticmethod
    def activate_student(student_id, teacher_id):
        alumno = Alumnos.query.filter_by(id=student_id, registered_by=teacher_id).first()
        if not alumno:
            return None, 'No tienes permiso para dar de alta a este alumno o el alumno no existe.'

        if alumno.activo:
            return None, 'El alumno ya ha sido dado de alta.'
        
        alumno.activo = True
        db.session.commit()
        return alumno, None
    
    @staticmethod
    def update_student(student_id, new_username, new_password, teacher_id):
        alumno = Alumnos.query.filter_by(id=student_id, registered_by=teacher_id).first()
        if not alumno:
            return None, 'No tienes permiso para editar a este alumno o el alumno no existe.'
        
        if not alumno.activo:
            return None, 'El alumno no está activo y no puede ser editado.'
        
        if new_username != alumno.username:
            if Alumnos.get_by_username(new_username):
                return None, 'Nombre de usuario en uso.'
        
        result, message = Alumnos.validate_password_format(new_password)
        if not result:
            return None, message

        alumno.username = new_username
        alumno.set_password(new_password)
        db.session.commit()
        return alumno, None
    
    #Return the number of active students
    @staticmethod
    def get_active_number_students():
        return Alumnos.query.filter_by(activo=True).count()