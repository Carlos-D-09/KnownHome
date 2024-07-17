from datetime import datetime
import string
import secrets

from ..db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import func, update
from sqlalchemy.orm import aliased, joinedload

from .maestros import Maestros
from .alumnos import Alumnos
from .grupo_alumno import Grupo_alumno

class Grupos (db.Model):
    __tablename__ = 'grupos'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    nombre = db.Column(db.NVARCHAR(50), unique = True)
    descripcion = db.Column(db.NVARCHAR(250))
    codigo_acceso = db.Column(db.NVARCHAR(6))
    activo = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    id_maestro = db.Column(INTEGER(unsigned=True), db.ForeignKey('maestros.id'), nullable=False)
    maestro = db.relationship('Maestros', backref=db.backref('grupo-maestro',lazy=True))

    def __init__(self, nombre, descripcion, id_maestro):
        self.nombre = nombre
        self.descripcion = descripcion
        self.codigo_acceso = Grupos.generate_code()
        self.id_maestro = id_maestro

    #Asocia la clase Maestros a la tabla maestros de la base de datos
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def generate_code():
        longitud = 6
        caracteres = string.ascii_uppercase + string.digits
        cadena_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        return cadena_aleatoria
    
    @staticmethod
    def get_active_group_by_code(codigo_acceso):
        return Grupos.query.filter_by(codigo_acceso=codigo_acceso, activo=True).first()
    
    def update(self, nuevo_nombre, nueva_descripcion):
        # Si el nombre es nuevo y no está vacío, actualízalo
        if nuevo_nombre and self.nombre != nuevo_nombre:
            if Grupos.is_name_unique(self.id, nuevo_nombre):
                self.nombre = nuevo_nombre
            else:
                raise ValueError("El nombre del grupo ya está en uso.")
        
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        
        db.session.commit()

    def delete(self):
        self.activo = False
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Grupos.query.get(id)
    
    @staticmethod
    def get_group(id_grupo, id_maestro):
        maestro_alias = aliased(Maestros)
        return (
            Grupos.query.with_entities(
                Grupos.id,
                Grupos.nombre,
                Grupos.descripcion,
                Grupos.codigo_acceso,
                Grupos.activo,
                func.date_format(Grupos.created_at, "%d-%m-%Y").label('created_at'),
                Grupos.id_maestro,
                maestro_alias.username.label('nombre_maestro')
            ).filter(
                (Grupos.id == id_grupo) &
                (Grupos.id_maestro == id_maestro) &
                (Grupos.activo == True)
            ).outerjoin(
                maestro_alias,
                Grupos.id_maestro == maestro_alias.id
            ).first()
        )

    # Get active groups by teacher
    @staticmethod
    def get_groups(maestro_id):
        grupo_alumno_alias = aliased(Grupo_alumno)
        maestro_alias = aliased(Maestros)
        return (
            Grupos.query
            .with_entities(
                Grupos.id,
                Grupos.nombre,
                Grupos.descripcion,
                func.date_format(Grupos.created_at, '%d-%m-%Y').label('created_at'),
                func.count(grupo_alumno_alias.id_grupo).label('num_alumnos'),
                maestro_alias.username.label('nombre_maestro')
            ).outerjoin(
                grupo_alumno_alias, 
                Grupos.id == grupo_alumno_alias.id_grupo,
            ).outerjoin(
                maestro_alias,
                Grupos.id_maestro == maestro_alias.id
            ).filter(
                (Grupos.id_maestro == maestro_id) & (Grupos.activo == True)
            ).group_by(
                Grupos.id
            ).order_by(
                func.coalesce(Grupos.created_at, '9999-12-31').asc()
            ).all()
        )

    @staticmethod
    def is_name_unique(id, new_name):
        existing_group = Grupos.query.filter(Grupos.nombre == new_name, Grupos.id != id).first()
        return existing_group is None
    
    @staticmethod
    def get_alumno_groups(id_alumno):
        return (
            Grupos.query
            .join(Grupo_alumno, Grupos.id == Grupo_alumno.id_grupo)
            .join(Maestros, Grupos.id_maestro == Maestros.id)
            .with_entities(
                Grupos.id,
                Grupos.nombre,
                Grupos.descripcion,
                Maestros.username.label('nombre_maestro')  
            )
            .filter(
                Grupo_alumno.id_alumno == id_alumno,
                Grupos.activo == True
            )
            .all()
        )
    
    @staticmethod
    def get_students_in_group(grupo_id):
        estudiantes = Grupo_alumno.query.filter_by(id_grupo=grupo_id).all()
    
        return [{'id_alumno': estudiante.alumno.id, 'nombre': estudiante.alumno.username} for estudiante in estudiantes if estudiante.alumno.activo == True]
    
    @staticmethod
    def get_enrolled_students(grupo_id):
        estudiantes = Grupo_alumno.query.join(Alumnos, Grupo_alumno.id_alumno == Alumnos.id).filter(Grupo_alumno.id_grupo == grupo_id).all()
        estudiantes_list = [{'id_alumno': estudiante.alumno.id, 'nombre': estudiante.alumno.username} for estudiante in estudiantes if estudiante.alumno.activo == True]
        return estudiantes_list
        
    @staticmethod
    def get_group_student(id_grupo, id_alumno):
        if not Grupo_alumno.is_student_enrolled(id_alumno, id_grupo):
            return None, 'No tienes derecho de ver la información de otros grupos en los que no estás inscrito.'

        grupo = (
            Grupos.query.with_entities(
                Grupos.id,
                Grupos.nombre.label('nombre_grupo'),
                Grupos.descripcion,
                Grupos.codigo_acceso,
                Grupos.activo,
                Grupos.id_maestro,
                Maestros.username.label('nombre_maestro') 
            ).join(
                Maestros, Grupos.id_maestro == Maestros.id 
            ).filter(
                Grupos.id == id_grupo,
                Grupos.activo == True
            ).first()
        )

        return grupo, None if grupo else 'Grupo no encontrado o inactivo'

    @staticmethod
    def descativate_teacher_groups(teacher_id):
        stmt = update(Grupos).where(Grupos.id_maestro == teacher_id).values(activo=False)
        db.session.execute(stmt)
        db.session.commit()
    
    @staticmethod
    def validate_name(name):
        if len(name) > 50:
            return False, 'El nombre no puede ser mayor a 50 caracteres'
        
        if len(name) == 0:
            return False, 'El nombre no puede estar vacio'

        return True, None
    
    @staticmethod
    def validate_desc(desc):
        if len(desc) > 250:
            return False, 'El nombre no puede ser mayor a 250 caracteres'
        
        if len(desc) == 0:
            return False, 'La descripción no puede estar vacía'

        return True, None
    
    @staticmethod
    def student_search_by_substring(substring, id_alumno):
        search = "%{}%".format(substring)
        grupos = (
            Grupos.query
            .join(Grupo_alumno, Grupos.id == Grupo_alumno.id_grupo)
            .join(Maestros, Grupos.id_maestro == Maestros.id)
            .filter(Grupos.nombre.ilike(search), Grupos.activo == True, Grupo_alumno.id_alumno == id_alumno)
            .with_entities(
                Grupos.id,
                Grupos.nombre,
                Maestros.username.label('username')
            )
            .all()
        )
        return [{'id': grupo.id, 'nombre': grupo.nombre, 'nombre_maestro': grupo.username} for grupo in grupos]
    
    @staticmethod
    def teacher_search_by_substring(substring, id_maestro):
        search = "%{}%".format(substring)
        grupos = (
            Grupos.query
            .filter(
                Grupos.nombre.ilike(search),
                Grupos.activo == True,
                Grupos.id_maestro == id_maestro
            )
            .with_entities(
                Grupos.id,
                Grupos.nombre,
                Grupos.descripcion,
                Maestros.username.label('nombre_maestro')
            )
            .join(Maestros, Grupos.id_maestro == Maestros.id)
            .all()
        )
        return [{'id': grupo.id, 'nombre': grupo.nombre, 'descripcion': grupo.descripcion, 'nombre_maestro': grupo.nombre_maestro} for grupo in grupos]
    
    @staticmethod
    def search_students_in_group(grupo_id, search_query):
        search = "%{}%".format(search_query)
        estudiantes = (Grupo_alumno.query
                    .join(Alumnos, Grupo_alumno.id_alumno == Alumnos.id)
                    .filter(Grupo_alumno.id_grupo == grupo_id, Alumnos.username.ilike(search))
                    .all())
        
        return [{'id_alumno': estudiante.alumno.id, 'nombre': estudiante.alumno.username} for estudiante in estudiantes if estudiante.alumno.activo == True] 

    @staticmethod
    def search_enrolled_students(grupo_id, search_query):
        search = "%{}%".format(search_query)
        estudiantes = (Grupo_alumno.query
                    .join(Alumnos, Grupo_alumno.id_alumno == Alumnos.id)
                    .filter(Grupo_alumno.id_grupo == grupo_id, Alumnos.username.ilike(search))
                    .all())

        return  [{'id_alumno': estudiante.alumno.id, 'nombre': estudiante.alumno.username} for estudiante in estudiantes if estudiante.alumno.activo == True]
        

    @staticmethod
    def get_active_number_groups():
        return Grupos.query.filter_by(activo=True).count()