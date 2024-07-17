from ..db import db
from sqlalchemy.dialects.mysql import INTEGER

class Incidencia(db.Model):
    __tablename__ = "incidencia"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    nombre = db.Column(db.NVARCHAR(50))
    descripcion = db.Column(db.NVARCHAR(250))
    recomendacion = db.Column(db.NVARCHAR(250))

    def __init__(self, nombre, descripcion, recomendacion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.recomendacion = recomendacion

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()