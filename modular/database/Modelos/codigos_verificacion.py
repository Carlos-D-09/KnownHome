from flask import current_app
from datetime import datetime

from ..db import db

import secrets
import string

import smtplib
from email.message import EmailMessage

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemyseeder import ResolvingSeeder


class Codigos_verificacion (db.Model):
    __tablename__ = 'codigos_verificacion'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    codigo = db.Column(db.NVARCHAR(6))
    correo = db.Column(db.NVARCHAR(150))
    fecha_creacion = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    used = db.Column(db.Boolean, default = False)

    id_usuario = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('verificacion-usuario',lazy=True))

    def __init__(self, correo, codigo, id_usuario, used=False):
        self.correo = correo
        self.codigo = codigo
        self.id_usuario = id_usuario
        self.used = used

    #Guarda el objeto en la entidad
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def resend_code(self):
        codigo = Codigos_verificacion.generate_code()

        email_sender = current_app.config['APP_EMAIL']
        email_sender_pwd = current_app.config['APP_EMAIL_PASSWORD']
        
        subject = "Código de verificación"
        body = "Hola " + self.user.username + ", este es tu código de verificación: " + codigo + ", tiene una duración de 1 hora, no lo comportas con nadie"
        

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = self.correo
        em["Subject"] = subject
        em.set_content(body)

        try:
            with smtplib.SMTP("smtp-mail.outlook.com",587) as smtp:
                smtp.starttls()
                smtp.login(email_sender, email_sender_pwd)
                smtp.sendmail(email_sender,self.correo, em.as_string())
                message = f"Correo enviado a {self.correo}, porfavor revisa tu bandeja de entrada y spam"
            return True, message, codigo
            
        except smtplib.SMTPException as e:
            message = (f"Error al enviar correo electrónico a {self.correo}, intente más tarde")
            return False, message, None

    def generate_code():
        longitud = 6
        caracteres = string.ascii_uppercase + string.digits
        cadena_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        return cadena_aleatoria

    @staticmethod
    def seed():
        file = "../Seeder/codigos_verificacion.json"
        seeder = ResolvingSeeder(db.session())
        new_entities = seeder.load_entities_from_json_file(file)
        db.session.commit()

    @staticmethod
    def send_verification_email(username, correo):
        codigo = Codigos_verificacion.generate_code()

        email_sender = current_app.config['APP_EMAIL']
        email_sender_pwd = current_app.config['APP_EMAIL_PASSWORD']
        
        subject = "Código de verificación"
        body = "Hola " + username + ", este es tu código de verificación: " + codigo + ", tiene una duración de 1 hora, no lo comportas con nadie"
        

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = correo
        em["Subject"] = subject
        em.set_content(body)

        try:
            with smtplib.SMTP("smtp-mail.outlook.com",587) as smtp:
                smtp.starttls()
                smtp.login(email_sender, email_sender_pwd)
                smtp.sendmail(email_sender,correo, em.as_string())
                message = f"Correo enviado a {correo}, porfavor revisa tu bandeja de entrada y spam"
            return True, message, codigo
            
        except smtplib.SMTPException as e:
            print(f"Error al enviar correo electrónico: {e}")
            message = (f"Error al enviar correo electrónico a {correo}, intente más tarde")
            return False, message, None

    @staticmethod
    def get_by_id(id):
        return Codigos_verificacion.query.get(id)
    
    @staticmethod
    def get_by_used(user_id):
        return Codigos_verificacion.query.filter_by(id_usuario=user_id, used=True).first()
    
    @staticmethod
    def get_by_not_used(user_id):
        return Codigos_verificacion.query.filter_by(id_usuario=user_id, used=False).first()


    