import os
from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    flash,  #Permite mandar mensajes de manera generica dentro de la aplicación
    render_template, request, url_for, session, current_app, redirect, g, jsonify,
    send_file
)

from database.Modelos.alumnos import Alumnos
from database.Modelos.grupos import Grupos

from auth import alumno_required, maestro_required

alumno = Blueprint('alumno', __name__, url_prefix='/alumno')

@alumno.route('/', methods=['GET'])
@alumno_required
def index():
    id_alumno = g.user.id
    grupos = Grupos.get_alumno_groups(id_alumno)
    grupos_list = [grupo._asdict() for grupo in grupos]
    return jsonify({'username': g.user.username, 'grupos': grupos_list})

@alumno.route('/register', methods=['POST'])
@maestro_required
def register():
    if request.method == 'POST':
        #Try to read the parameters form the request
        try:
            username = request.form["username"]
            password = request.form["password"]

        except:
            return jsonify({'error':True, 'message': 'Paramestros recibidos invalidos'})
        
        if not username:
            return jsonify({'error': True, 'message': 'El nombre de usuario no puede estar vacío'})
        
        #Check uniquess of record 
        if Alumnos.get_by_username(username):
            return jsonify({'error':True, 'message': 'Nombre de usuario en uso'})

        result, message = Alumnos.validate_password_format(password)

        if not result:
            return jsonify({'error':True, 'message': message})

        #Create new user
        alumno = Alumnos(username, password, g.user.id)
        alumno.save()
        alumno.create_directory()

        return jsonify({'error': False, 'message': 'Alumno registrado exitosamente'})

# Editar las credenciales del estudiante siendo el maestro que lo registró
@alumno.route('/edit-student/<int:student_id>', methods=['PUT'])
@maestro_required
def edit_student(student_id):
    try:
        new_username = request.form["username"].strip()
        new_password = request.form["password"]
    except:
        return jsonify({'error': True, 'message': 'Parámetros recibidos inválidos'}), 400

    if not new_username:
        return jsonify({'error': True, 'message': 'El nombre de usuario no puede estar vacío'}), 400

    id_maestro = g.user.id  # Obtener el ID del maestro desde el contexto de la aplicación
    alumno, error_message = Alumnos.update_student(student_id, new_username, new_password, id_maestro)
    
    if error_message:
        return jsonify({'error': True, 'message': error_message}), 400
    
    return jsonify({'error': False, 'message': 'Alumno actualizado exitosamente.'}), 200

# Mostrar los todos los alumnos registrados por mi en estatus de activo
@alumno.route('/active-students', methods=['GET'])
@maestro_required
def active_students_list():
    id_maestro = g.user.id  
    estudiantes = Alumnos.get_active_students_by_teacher(id_maestro)
    
    if not estudiantes:
        return jsonify({'error': True, 'message': 'No se encontraron alumnos activos registrados por este maestro.'})
    
    return jsonify({'error': False, 'estudiantes': estudiantes}), 200

# Mostrar los todos los alumnos registrados por mi en estatus de inactivo
@alumno.route('/inactive-students', methods=['GET'])
@maestro_required
def inactive_students_list():
    id_maestro = g.user.id  # Obtener el ID del maestro desde el contexto de la aplicación
    estudiantes = Alumnos.get_inactive_students_by_teacher(id_maestro)
    
    if not estudiantes:
        return jsonify({'error': True, 'message': 'No se encontraron alumnos inactivos registrados por este maestro.'})
    
    return jsonify({'error': False, 'estudiantes': estudiantes}), 200

# Buscar los alumnos que están registrados por mi
@alumno.route('/my-students', methods=['GET'])
@maestro_required
def my_students_list():
    search_query = request.args.get('query', '').strip()
    id_maestro = g.user.id 
    estudiantes = Alumnos.search_students_registered_by_teacher(id_maestro, search_query)
    
    if not estudiantes:
        return jsonify({'error': True, 'message': 'No se encontraron alumnos registrados que coincidan con la búsqueda.'})
    
    return jsonify({'error': False, 'estudiantes': estudiantes}), 200

# Ver los alumnos que hayan sido dados de baja por mi
@alumno.route('/deactivated-students', methods=['GET'])
@maestro_required
def deactivated_students_list():
    search_query = request.args.get('query', '').strip()
    id_maestro = g.user.id  # Obtener el ID del maestro desde el contexto de la aplicación
    estudiantes = Alumnos.search_deactivated_students_by_teacher(id_maestro, search_query)
    
    if not estudiantes:
        return jsonify({'error': True, 'message': 'No se encontraron alumnos dados de baja que coincidan con la búsqueda.'})
    
    return jsonify({'error': False, 'estudiantes': estudiantes}), 200

# Dar de baja a alumno en la plataforma
@alumno.route('/deactivate-student/<int:student_id>', methods=['DELETE'])
@maestro_required
def deactivate_student(student_id):
    id_maestro = g.user.id  
    alumno, error_message = Alumnos.deactivate_student(student_id, id_maestro)
    
    if error_message:
        return jsonify({'error': True, 'message': error_message}), 400
    
    return jsonify({'error': False, 'message': 'El alumno ha sido dado de baja exitosamente.'}), 200

# Dar de alta a alumno en la plataforma (que haya sido dado de baja con anterioridad)
@alumno.route('/activate-student/<int:student_id>', methods=['POST'])
@maestro_required
def activate_student(student_id):
    id_maestro = g.user.id  # Obtener el ID del maestro desde el contexto de la aplicación
    alumno, error_message = Alumnos.activate_student(student_id, id_maestro)
    
    if error_message:
        return jsonify({'error': True, 'message': error_message}), 400
    
    return jsonify({'error': False, 'message': 'El alumno ha sido dado de alta exitosamente.'}), 200

# Previsualizar el archivo
@alumno.route('/preview-file', methods=['POST'])
@maestro_required
def preview_file():
    file = request.files['file']
    if not file:
        return jsonify({'error': True, 'message': 'Archivo no proporcionado'})

    content = file.read().decode('utf-8').strip()
    registros = content.split('\n')  # Divide el contenido del archivo en líneas individuales

    return jsonify({'contenido': registros})
    

# Registrar muchos alumnos mediante txt (txt manipulado en el front y pasado a un json)
@alumno.route('/bulk-register', methods=['POST'])
@maestro_required
def bulk_register():
    alumnos_data = request.json.get('alumnos', [])
    resultados = []

    for alumno_data in alumnos_data:
        username = alumno_data.get('username')
        password = alumno_data.get('password')

        if not username or not password:
            resultados.append({'username': username, 'error': 'Faltan campos requeridos'})
            continue

        if Alumnos.get_by_username(username):
            resultados.append({'username': username, 'error': 'Nombre de usuario en uso'})
            continue

        result, message = Alumnos.validate_password_format(password)
        if not result:
            resultados.append({'username': username, 'error': message})
            continue

        hashed_pwd = Alumnos.generate_password(password)
        nuevo_alumno = Alumnos(username=username, password=hashed_pwd, registered_by=g.user.id)
        nuevo_alumno.save()
        nuevo_alumno.create_directory()

        resultados.append({'username': username, 'message': 'Alumno registrado exitosamente'})

    # Devolver los resultados como un JSON
    return jsonify(resultados), 200