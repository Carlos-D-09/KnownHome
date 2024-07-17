from ..db import db
from datetime import datetime

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemyseeder import ResolvingSeeder

class Passwords_antiguas (db.Model):
    __tablename__ = 'passwords_antiguas'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    fecha_cambio = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    password_antigua = db.Column(db.NVARCHAR(256))

    id_usuario = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('password-usuario',lazy=True))


    def __init__(self, password_antigua, id_usuario):
        self.password_antigua = password_antigua
        self.id_usuario = id_usuario

    #Asocia la clase Cambios_password a la tabla codigos verificacion de la base de datos
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Passwords_antiguas.query.get(id)
    
    @staticmethod
    def get_by_user(id_usuario):
        return Passwords_antiguas.query.with_entities(
                Passwords_antiguas.password_antigua
            ).filter(
                Passwords_antiguas.id_usuario == id_usuario
            ).all()