from ..db import db

from sqlalchemy.dialects.mysql import INTEGER

from .incidencia import Incidencia

class Objetos (db.Model):
    __tablename__ = 'objetos'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    objeto = db.Column(db.NVARCHAR(100))

    id_incidencia = db.Column(INTEGER(unsigned=True), db.ForeignKey('incidencia.id'), nullable=True)
    incidencia = db.relationship('Incidencia', backref=db.backref('objeto_incidencia', lazy=True))

    #Asocia la clase Clasicacion_objetos a la tabla codigos verificacion de la base de datos
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Objetos.query.get(id)
    
    @staticmethod
    def get_by_object(object_name):
        return Objetos.query.filter_by(objeto=object_name).first()

    @staticmethod
    def get_all():
        return Objetos.query.all()