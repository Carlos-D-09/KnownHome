import os
from ..db import db

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import desc, select, func
from sqlalchemy.orm import aliased

# Assuming Users and Objets models are defined elsewhere
from .maestros import Maestros
from .alumnos import Alumnos
from .grupos import Grupos
from .objetos import Objetos
from .objetos import Incidencia

from sqlalchemy import func

class Imagenes_escaneadas(db.Model):
    __tablename__ = 'imagenes_escaneadas'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    nombre = db.Column(db.NVARCHAR(50))
    ruta = db.Column(db.NVARCHAR(512))
    autorizada = db.Column(db.Boolean)
    clasificada = db.Column(db.Boolean)
    clasificacion_correcta = db.Column(db.Boolean, nullable=True)

    id_maestro = db.Column(INTEGER(unsigned=True), db.ForeignKey('maestros.id'), nullable=True)
    user_maestro = db.relationship('Maestros', backref=db.backref('imagenes_maestro', lazy=True))

    id_alumno = db.Column(INTEGER(unsigned=True), db.ForeignKey('alumnos.id'), nullable=True)
    user_alumno = db.relationship('Alumnos', backref=db.backref('imagenes_alumno', lazy=True))

    id_grupo = db.Column(INTEGER(unsigned=True), db.ForeignKey('grupos.id'), nullable=False)
    grupo = db.relationship('Grupos', backref=db.backref('imagenes_grupo', lazy=True))

    id_objeto = db.Column(INTEGER(unsigned=True), db.ForeignKey('objetos.id'), nullable=True)
    objeto_clasificado = db.relationship('Objetos', backref=db.backref('imagen_objeto', lazy=True))

    def __init__(self, id_grupo, nombre, ruta, autorizada=False, clasificada=False, clasificacion_correcta=None, id_alumno=None, id_maestro=None, id_objeto=None):
        self.id_grupo = id_grupo
        self.nombre = nombre
        self.ruta = ruta
        self.autorizada = autorizada
        self.clasificada = clasificada
        self.clasificacion_correcta = clasificacion_correcta
        
        if id_alumno != None:
            self.id_alumno = id_alumno

        if id_maestro != None: 
            self.id_maestro = id_maestro

        self.id_objeto = id_objeto

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        try:
            # Verificar si la ruta es absoluta o relativa y construir la ruta completa
            if not os.path.isabs(self.ruta):
                full_path = os.path.join(os.getcwd(), 'modular/static', self.ruta.lstrip('/'))
            else:
                full_path = self.ruta
            
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            print(f"Error deleting file {self.ruta}: {e}")
        
        db.session.delete(self)
        db.session.commit()

    def authorize(self):
        self.autorizada = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(image_id):
        return Imagenes_escaneadas.query.filter_by(id=image_id).first()

    @staticmethod
    def get_all_images():
        return Imagenes_escaneadas.query.filter(
                Imagenes_escaneadas.clasificada==True,
                Imagenes_escaneadas.clasificacion_correcta.isnot(None)
            ).order_by(
                desc(Imagenes_escaneadas.id)
            ).all()
    
    @staticmethod
    def get_images_by_group(group_id):
        return Imagenes_escaneadas.query.filter(
                Imagenes_escaneadas.id_grupo == group_id,
                Imagenes_escaneadas.clasificada == True,
                Imagenes_escaneadas.clasificacion_correcta.isnot(None)
            ).order_by(
                desc(Imagenes_escaneadas.id)
            ).all()
    
    @staticmethod
    def get_dict_images_by_group(group_id):
        grupo_alias = aliased(Grupos)
        alumno_alias = aliased(Alumnos)
        maestro_alias = aliased(Maestros)
        objeto_alias = aliased(Objetos)
        incidencia_alias = aliased(Incidencia)
        return db.session.query(
            Imagenes_escaneadas.id,
            Imagenes_escaneadas.ruta,
            Imagenes_escaneadas.clasificacion_correcta,
            grupo_alias.nombre.label('group'),
            alumno_alias.username.label('alumno'),
            maestro_alias.username.label('maestro'),
            objeto_alias.objeto.label('objeto'),
            incidencia_alias.nombre.label('riesgo')
        ).select_from(
            Imagenes_escaneadas
        ).outerjoin(
            grupo_alias,
            Imagenes_escaneadas.id_grupo == grupo_alias.id
        ).outerjoin(
            alumno_alias,
            Imagenes_escaneadas.id_alumno == alumno_alias.id
        ).outerjoin(
            maestro_alias,
            Imagenes_escaneadas.id_maestro == maestro_alias.id
        ).outerjoin(
            objeto_alias,
            Imagenes_escaneadas.id_objeto == objeto_alias.id
        ).outerjoin(
            incidencia_alias,
            objeto_alias.id_incidencia == incidencia_alias.id
        ).filter(
            Imagenes_escaneadas.id_grupo == group_id
        ).order_by(
            desc(Imagenes_escaneadas.id)
        ).all()

    @staticmethod
    def get_images_by_object(id_objeto):
        return Imagenes_escaneadas.query.filter_by(id_objeto=id_objeto, clasificada=True).all()
    
    @staticmethod
    def get_images_by_student_and_group(cls, student_id, group_id):
        return cls.query.filter_by(
            id_alumno=student_id, 
            id_grupo=group_id
            ).order_by(
                desc(Imagenes_escaneadas.id)
            ).all()
    
    @staticmethod
    def get_image_by_id_group_and_student(cls, photo_id, group_id, student_id):
        return cls.query.filter_by(id=photo_id, id_grupo=group_id, id_alumno=student_id).first()
    
    @staticmethod
    def get_authorized_images_by_student_and_group(student_id, group_id):
        return Imagenes_escaneadas.query.filter_by(
            id_alumno=student_id, 
            id_grupo=group_id, 
            autorizada=True
        ).order_by(
            desc(Imagenes_escaneadas.id)
        ).all()
    
    @staticmethod
    def get_teacher_images_by_group(group_id, teacher_id):
        return Imagenes_escaneadas.query.filter_by(
            id_grupo=group_id, 
            id_maestro=teacher_id
        ).order_by(
            desc(Imagenes_escaneadas.id)
        ).all()
    
    @staticmethod
    def get_teacher_authorized_images_by_group(group_id, teacher_id):
        return Imagenes_escaneadas.query.filter_by(
            id_grupo=group_id, 
            id_maestro=teacher_id,
            autorizada=1
        ).order_by(
            desc(Imagenes_escaneadas.id)
        ).all()

    @staticmethod
    def get_specific_teacher_image(cls, group_id, photo_id, teacher_id):
        return cls.query.filter_by(id=photo_id, id_grupo=group_id, id_maestro=teacher_id).first()
    