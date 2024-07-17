from ..db import db

from sqlalchemy import and_
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import aliased

from .alumnos import Alumnos

class Grupo_alumno (db.Model):
    __tablename__ = 'grupo_alumno'

    id_alumno = db.Column(INTEGER(unsigned=True), db.ForeignKey('alumnos.id'), nullable=False, primary_key=True)
    alumno = db.relationship('Alumnos', backref=db.backref('alumno-grupo',lazy=True))
    
    id_grupo = db.Column(INTEGER(unsigned=True), db.ForeignKey('grupos.id'), nullable=False, primary_key=True)
    grupo = db.relationship('Grupos', backref=db.backref('grupo-alumno',lazy=True))

    __table_args__ = (
        db.PrimaryKeyConstraint('id_alumno','id_grupo'),
    )

    def __init__(self, id_alumno, id_grupo):
        self.id_alumno = id_alumno
        self.id_grupo = id_grupo

    #Asocia la clase Maestros a la tabla maestros de la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_alumno, id_grupo):
        return Grupo_alumno.query.filter_by(id_alumno=id_alumno, id_grupo=id_grupo).first()

    @staticmethod
    def is_student_enrolled(id_alumno, id_grupo):
        result = Grupo_alumno.query.filter_by(id_alumno=id_alumno, id_grupo=id_grupo).first()
        return result is not None

    @staticmethod
    def get_students_enrolled(id_grupo):
        alumno_alias = aliased(Alumnos)
        students_list = []

        students = Grupo_alumno.query.filter(alumno_alias.activo==True).with_entities(
            alumno_alias.id.label('student_id'),
            alumno_alias.username.label('student_username')
        ).join(
            Grupo_alumno,
            and_(
                Grupo_alumno.id_alumno == alumno_alias.id,
                Grupo_alumno.id_grupo == id_grupo
            )
        ).all()

        for student in students:
            student_dict = {
                'student_id': student.student_id,
                'student_username': student.student_username
            }
            students_list.append(student_dict)

        return students_list