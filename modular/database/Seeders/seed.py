import os

import click
from flask.cli import with_appcontext
from sqlalchemyseeder import ResolvingSeeder
from sqlalchemy.exc import SQLAlchemyError

from ..db import db
from ..Modelos.usuarios import Users
from ..Modelos.maestros import Maestros
from ..Modelos.grupos import Grupos
from ..Modelos.grupo_alumno import Grupo_alumno
from ..Modelos.alumnos import Alumnos
from ..Modelos.codigos_verificacion import Codigos_verificacion
from ..Modelos.incidencia import Incidencia
from ..Modelos.objetos import Objetos
from ..Modelos.imagenes_escaneadas import Imagenes_escaneadas

def configure_seed(app):
    app.cli.add_command(seed_db)
    app.cli.add_command(seed_images)

def seed_supervisor():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Users)
        seeder.register_class(Codigos_verificacion)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'users', 'user.json'))
        db.session.commit()
        seeder.load_entities_from_json_file(os.path.join(current_dir, 'users', 'codigos_verificacion.json'))
        db.session.commit()
        click.echo("Supervisor users seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Error trying to seed supervisor users: {e}")

def seed_admin():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Users)
        seeder.register_class(Codigos_verificacion)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'users', 'users_admin.json'))
        db.session.commit()
        seeder.load_entities_from_json_file(os.path.join(current_dir, 'users','codigos_verificacion_admin.json'))
        db.session.commit()
        click.echo("Administrator users seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Error trying to seed administrator users: {e}")

def seed_teachers():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Maestros)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'teachers', 'teachers.json'))
        db.session.commit()

         # Obtener los maestros cargados
        teachers = Maestros.query.all()

        # Crear directorios para cada maestro
        for teacher in teachers:
            teacher.create_directory()

        click.echo("Maestros table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed teachers: {e}") 

def seed_groups():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Grupos)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'groups', 'groups.json'))
        db.session.commit()
        click.echo("Grupos table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed groups: {e}") 

def seed_students():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Alumnos)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'students', 'students.json'))
        db.session.commit()

        # Obtener los maestros cargados
        students = Alumnos.query.all()

        # Crear directorios para cada maestro
        for student in students:
            student.create_directory()

        click.echo("Alumnos table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed students: {e}") 

def seed_group_students():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Grupo_alumno)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'group_student', 'group_student.json'))
        db.session.commit()
        click.echo("Grupo-alumno table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed students: {e}") 

def seed_incidencia():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Incidencia)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'incidencia', 'incidencia.json'))
        db.session.commit()
        click.echo("Incidencia table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed incidencia: {e}") 

def seed_objetos():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Objetos)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'objetos', 'objetos.json'))
        db.session.commit()
        click.echo("Objetos table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed objetos: {e}") 

@click.command('seed-images')
@with_appcontext
def seed_images():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeder = ResolvingSeeder(db.session)
        seeder.register_class(Objetos)
        seeder.register_class(Imagenes_escaneadas)

        seeder.load_entities_from_json_file(os.path.join(current_dir, 'images', 'images.json'))
        db.session.commit()
        click.echo("Images table seeded successfully")
    except SQLAlchemyError as e:
        click.echo(f"Eror trying to seed images: {e}") 

@click.command('seed-db')
@with_appcontext
def seed_db():
    seed_incidencia()
    seed_objetos()
    seed_supervisor()
    seed_admin()
    seed_teachers()
    seed_students()
    seed_groups()
    seed_group_students()
    # seed_images()
    click.echo("Database seeded successfully")