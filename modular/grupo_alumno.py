from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    render_template, request, url_for, g, jsonify
)
from database.Modelos.grupos import Grupos
from database.Modelos.grupo_alumno import Grupo_alumno

from auth import maestro_required
from auth import alumno_required

grupo_alumno = Blueprint('grupo_alumno', __name__, url_prefix='/grupo-alumno')

@grupo_alumno.route('/join-group', methods=['POST'])
@alumno_required
def join_group():
    codigo_acceso = request.form['codigo_acceso']
    id_alumno = g.user.id  

    grupo = Grupos.get_active_group_by_code(codigo_acceso)
    if not grupo:
        return jsonify({'error': True, 'message': 'Código de acceso inválido'}), 404

    existing_registro = Grupo_alumno.get_by_id(id_alumno=id_alumno, id_grupo=grupo.id)
    if existing_registro:
        return jsonify({'error': True, 'message': 'Ya estás registrado en el grupo'}), 409

    nuevo_registro = Grupo_alumno(id_alumno=id_alumno, id_grupo=grupo.id)
    nuevo_registro.save()

    return jsonify({'error': False, 'message': 'Te has registrado en el grupo exitosamente', 'nombre_grupo': grupo.nombre})

@grupo_alumno.route('/grupo/<int:grupo_id>', methods=['GET'])
@alumno_required
def get_group_student(grupo_id):
    grupo, mensaje_error = Grupos.get_group_student(grupo_id, g.user.id)
    
    if grupo:
        grupo = [grupo._asdict()]
        return jsonify({'error': False, 'grupo': grupo}), 200
    else:
        return jsonify({'error': True, 'mensaje': mensaje_error}), 403
    
@grupo_alumno.route('/student-search-groups', methods=['GET'])
@alumno_required
def search_groups():
    query = request.args.get('query', '').strip()
    
    id_alumno = g.user.id 
    grupos = Grupos.student_search_by_substring(query, id_alumno)
    
    if not grupos:
        return jsonify({'error': True, 'message': 'No se encontraron grupos.'})
    
    return jsonify({'error': False, 'grupos': grupos}), 200

@grupo_alumno.route('/teacher-search-groups', methods=['GET'])
@maestro_required
def teacher_search_groups():
    query = request.args.get('query', '').strip()
    
    id_maestro = g.user.id 
    grupos = Grupos.teacher_search_by_substring(query, id_maestro)
    
    if not grupos:
        return jsonify({'error': True, 'message': 'No se encontraron grupos.'})
    
    return jsonify({'error': False, 'grupos': grupos}), 200

@grupo_alumno.route('/<int:id_grupo>/students', methods=['GET'])
@alumno_required
def student_get_students_from_group(id_grupo):
    id_alumno = g.user.id
    student_group_register = Grupo_alumno.get_by_id(id_alumno,id_grupo)

    # Evaluate the current logged student is register in the group
    if not student_group_register:
        return jsonify({'error': True, 'mensaje': 'El alumno no esta registrado en el grupo'})
    
    students = Grupos.get_students_in_group(id_grupo)
    
    if not students:
        return jsonify({'error': True, 'message': 'No existen estudiantes'})
    
    return jsonify({'estudiantes': students})

@grupo_alumno.route('/<int:grupo_id>/enrolled-students', methods=['GET'])
@maestro_required
def teacher_get_students_from_group(grupo_id):
    id_maestro = g.user.id  
    grupo = Grupos.get_by_id(grupo_id)

    # Evaluate the group exist, it's active and belongs to the logged teacher
    if not grupo or grupo.activo == False or grupo.id_maestro != id_maestro:
        return jsonify({'error': True, 'mensaje': 'Grupo no encontrado, no está activo, o no pertenece al maestro'})
    
    students = Grupos.get_enrolled_students(grupo_id)

    if len(students) == 0:
        return jsonify({'error': True, 'mensaje': 'El grupo esta vacío'})
    
    return jsonify({'error': False, 'estudiantes': students})

@grupo_alumno.route('/<int:id_grupo>/search-students', methods=['GET'])
@alumno_required
def student_search_students_from_group(id_grupo):
    search_query = request.args.get('query', '').strip()
    id_alumno = g.user.id
    student_group_register = Grupo_alumno.get_by_id(id_alumno, id_grupo)

    # Evaluate the current logged student is register in the group
    if not student_group_register:
        return jsonify({'error': True, 'mensaje': 'El alumno no esta registrado en el grupo'})

    #Evaluate that the search term is not empty 
    if not search_query:
        return jsonify({'error': True, 'message': 'Debe proporcionar una subcadena para la búsqueda'}), 400

    #Search the query in the username students register
    students = Grupos.search_students_in_group(id_grupo, search_query)

    if not students:
        return jsonify({'error': True, 'mensaje': 'No hay alumnos que coincidan con la búsqueda en el grupo'}) 

    return jsonify({'error': False,'estudiantes': students})


@grupo_alumno.route('/<int:grupo_id>/search-enrolled-students', methods=['GET'])
@maestro_required
def teacher_search_students_from_group(grupo_id):
    search_query = request.args.get('query', '').strip()
    id_maestro = g.user.id  
    grupo = Grupos.get_by_id(grupo_id)

    # Evaluate the group exist, it's active and belongs to the logged teacher
    if not grupo or grupo.activo == False or grupo.id_maestro != id_maestro:
        return jsonify({'error': True, 'mensaje': 'Grupo no encontrado, no está activo, o no pertenece al maestro'})
    
    #Evaluate that the search term is not empty 
    if not search_query:
        return jsonify({'error': True, 'message': 'Debe proporcionar una subcadena para la búsqueda'}), 400

    students = Grupos.search_enrolled_students(grupo_id, search_query)

    if not students:
        return jsonify({'error': True, 'message': 'No existen coincidencias'}), 400

    return jsonify({'estudiantes': students})

@grupo_alumno.route('/student-leave-group', methods=['DELETE'])
@alumno_required
def student_leave_group():
    id_grupo = request.form['id_grupo']
    id_alumno = g.user.id  

    registro_grupo_alumno = Grupo_alumno.get_by_id(id_alumno, id_grupo)
    if not registro_grupo_alumno:
        return jsonify({'error': True, 'message': 'No estas registrado en el grupo'}), 404

    registro_grupo_alumno.delete()

    return jsonify({'error': False, 'message': 'Has salido del grupo.'})

@grupo_alumno.route('/teacher-remove-student', methods=['DELETE'])
@maestro_required
def teacher_remove_student():
    id_alumno = request.form['id_alumno']
    id_grupo = request.form['id_grupo']

    grupo = Grupos.get_by_id(id_grupo)
    if not grupo or grupo.id_maestro != g.user.id:
        return jsonify({'error': True, 'message': 'Operación no permitida. El grupo no pertenece al maestro.'}), 403
    
    registro_grupo_alumno = Grupo_alumno.get_by_id(id_alumno, id_grupo)
    if not registro_grupo_alumno:
        return jsonify({'error': True, 'message': 'El alumno no está registrado en el grupo'}), 404

    registro_grupo_alumno.delete()

    return jsonify({'error': False, 'message': 'El alumno ha sido eliminado del grupo'})