from flask import (
    Blueprint, g, request, jsonify, session, json
)

from modular.auth import login_user_web_required, supervisor_required, administrador_required

from .database.Modelos.usuarios import Users
from .database.Modelos.maestros import Maestros
from .database.Modelos.grupos import Grupos
from .database.Modelos.grupo_alumno import Grupo_alumno
from .database.Modelos.alumnos import Alumnos
from .database.Modelos.objetos import Objetos
from .database.Modelos.imagenes_escaneadas import Imagenes_escaneadas
from .database.Modelos.passwords_antiguas import Passwords_antiguas

api_user = Blueprint('api_user', __name__, url_prefix='/user/api')

#Get user profile general info (id, username, correo, rol)
@api_user.route('/profile', methods=['GET'])
@login_user_web_required
def get_user_info():
    if request.method == 'GET':
        try:
            user = Users.get_general_info(g.user.id)
            if user != None:
                return jsonify({'error': False, 'user':user._asdict()})

            return jsonify({'error':True, 'message': 'No existe el usuario'})
    
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get all the administrator users created by the current supervisor user logged 
@api_user.route("/admin_users", methods=['GET'])
@supervisor_required
def admin_users_api():
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            users = user.get_admin_users()
            users_list = [aux._asdict() for aux in users]
            return jsonify({'error':False, 'users':users_list})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})


#Get administrator user info. Using supervisor user
@api_user.route("/admin_user/<int:id_usuario>", methods=['GET'])
@supervisor_required
def admin_user_api(id_usuario):
    if request.method == 'GET':
        try:
            user = Users.get_general_info_admin(id_usuario)        
            if not user:
                return jsonify({'error':True, 'message': 'No existe el usuario'});
            
            return jsonify({'error':False, 'user':user._asdict()})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Edit x administrator user. Using supervisor user
@api_user.route("/admin_user/edit/<int:id_usuario>", methods=['PUT'])
@supervisor_required
def admin_user_edit_api(id_usuario):
    if request.method == 'PUT':
        try:
            form = request.get_json();
            username = form['username']
            email = form['email']
            password = form['password']
        
            user = Users.get_by_id(id_usuario)
            if not user:
                return jsonify({'error':True, 'message': 'No existe el usuario'})
            
            #Validate new username (format and availability)
            valid_username, username_msg = user.validate_new_username(username)
            
            #Validate new email (format and availability)
            valid_email, email_msg = user.validate_new_email(email)
            
            if not valid_username: 
                if user.username != username:
                    return jsonify({'error': True, 'message':username_msg})
            else:
                if user.username != username:
                    user.set_new_username(username)
            
            if not valid_email:
                if user.correo != email:
                    return jsonify({'error': True, 'message':email_msg})
            else:
                if user.correo != email:
                    user.set_new_email(email)

            if password != '':
                #Verify if the new password is not the current password
                if not user.check_password(password):
                    #Verify if the passwaord hasn't been use
                    if user.check_old_passwords(password):
                        return jsonify({'error': True, 'message':'Esta contraseña ya ha sido utilizada en este perfil, no se puede volver a registrar'})
                    
                    #Validate password format
                    if len(password) < 8:
                        return jsonify({'error': True, 'message':'La contraseña no puede ser menor a 8 caracteres'})
                    if not Users.validate_password_format(password):
                        return jsonify({'error': True, 'message':'La contraseña debe contener una letra mayuscula, una minuscula, un númeor y un símbolo'})
                    
                    #Register de current password as used
                    old_password = Passwords_antiguas(user.password, user.id)
                    old_password.save()

                    #Change password
                    user.set_new_password(password)

            return jsonify({'error':False, 'message':'Usuario editado exitosamente'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Delete x administrator user. Using a supervisor user
@api_user.route("/admin_user/delete/<int:id_usuario>", methods=['DELETE'])
@supervisor_required
def delete_user_api(id_usuario):
    if request.method == 'DELETE':
        try:
            user = Users.get_general_info_admin(id_usuario)
            if not user:
                return jsonify({'error':True, 'message': 'No existe el usuario'})
            
            user = Users.get_by_id(id_usuario)
            user.desactivate()
            
            return jsonify({'error':False, 'message': 'Usuario eliminado con exito'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Route to search by name or email an administrator user. Using supervisor user
@api_user.route("/admin_user/search", methods=['GET'])
@supervisor_required
def admin_user_search():
    if request.method == 'GET':
        try:
            word = request.args['search_term']
            users = Users.search_admin_user(word)
            users_list = [aux._asdict() for aux in users]
            return jsonify({'error':False, 'users':users_list})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get all the teachers users created by the current user logged. Using administrator user
@api_user.route("/admin_teachers", methods=['GET'])
@administrador_required
def admin_teachers_api():
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            teachers = user.get_user_teachers()
            teachers_list = [aux._asdict() for aux in teachers]
            return jsonify({'error':False, 'teachers':teachers_list})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get general info for x teacher. Using administrator user
@api_user.route("/admin_teacher/<int:id_teacher>", methods=['GET'])
@administrador_required
def admin_teacher_api(id_teacher):
    if request.method == 'GET':
        try:
            teacher = Maestros.get_general_info_teacher(id_teacher)        
            if not teacher:
                return jsonify({'error':True, 'message': 'No existe el maestro'});
            
            if teacher.registered_by != g.user.id:
                return jsonify({'error':True, 'message': 'No tienes permisos para modificar este usuario'});

            return jsonify({'error':False, 'teacher':teacher._asdict()})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Search by name or email an administrator user
@api_user.route("/admin_teacher/search", methods=['GET'])
@administrador_required
def teacher_user_search_api():
    if request.method == 'GET':
        try:
            search_term = request.args['search_term']
            user = Users.get_by_id(g.user.id)
            teachers = user.search_teacher_username(search_term)
            teachers_list = [aux._asdict() for aux in teachers]

            return jsonify({'error':False, 'teachers':teachers_list})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Edit x teacher using an administrator user
@api_user.route("/admin_teacher/edit/<int:id_teacher>", methods=['PUT'])
@administrador_required
def admin_teacher_edit_api(id_teacher):
    if request.method == 'PUT':
        try:
            form = request.get_json();
            username = form['username']
            password = form['password']
        
            teacher = Maestros.get_by_id(id_teacher)

            if not teacher:
                return jsonify({'error':True, 'message': 'No existe el usuario'})

            #Validate teacher username format
            valid_username, username_msg = teacher.validate_new_username(username)
            if not valid_username: 
                if teacher.username != username:
                    return jsonify({'error': True, 'message':username_msg})
            else:
                if teacher.username != username:
                    teacher.set_new_username(username)
            
            #Validate password format
            if password != '':
                if not teacher.check_password(password):
                    valid_password, msg = Maestros.validate_password_format(password)
                    if not valid_password:
                        return jsonify({'error': True, 'message':msg})
                    
                    teacher.set_new_password(password)

            return jsonify({'error':False, 'message':'Usuario editado exitosamente'})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Delete x teacher. Using administrator user
@api_user.route("/admin_teacher/delete/<int:id_teacher>", methods=['DELETE'])
@administrador_required
def delete_teacher_api(id_teacher):
    if request.method == 'DELETE':
        try:
            teacher = Maestros.get_general_info_teacher(id_teacher)
            if not teacher:
                return jsonify({'error':True, 'message': 'No existe el maestro'})
            
            if teacher.registered_by != g.user.id:
                return jsonify({'error':True, 'message': 'No tienes los permisos suficientes parar realizar esta operacíon'})
            
            teacher = Maestros.get_by_id(id_teacher)
            teacher.desactivate()
            Grupos.descativate_teacher_groups(id_teacher)
            return jsonify({'error':False, 'message': 'Usuario eliminado con exito'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get all the groups create by the teachers registered by the current user
@api_user.route("/admin_groups", methods=['GET'])
@administrador_required
def admin_groups_api():
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            #Get the teachers registered by the current user
            my_teachers = user.get_user_teachers()

            #List to save the groups
            grupos = []

            for teacher in my_teachers: 
                #Recover the groups owned by the current teacher
                my_groups = Grupos.get_groups(teacher.id)
                grupos.extend(my_groups)

            grupos_list = [grupo._asdict() for grupo in grupos]
                
            return jsonify({'error':False, 'groups':grupos_list})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get group info (id, nombre, descripcion, id_maestro)
@api_user.route("/admin_groups/<int:id_grupo>", methods=['GET'])
@administrador_required
def get_group_info_api(id_grupo):
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)

            if not group:
                return jsonify({'error':True,'message':'No existe el grupo que estas tratando de editar'})

            if user.validate_group(group.id): 
                group_attr = {
                    "id": group.id,
                    "nombre": group.nombre,
                    "descripcion": group.descripcion,
                    "created_at": group.created_at.strftime('%d-%m-%Y'),
                    "id_maestro": group.id_maestro,
                    "maestro": group.maestro.username
                }
                return jsonify({'error':False, 'group':group_attr})
            else:
                return jsonify({'error':True, 'message':'No tienes permisos suficientes para acceder a la información del grupo'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Edit x group info ( nombre, descripcion)
@api_user.route("/admin_groups/<int:id_grupo>/edit", methods=['PUT'])
@administrador_required
def edit_group_api(id_grupo):
    if request.method == 'PUT':
        try:
            form = request.get_json()
            name = form['name']
            desc = form['desc']
            
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)

            if not group:
                return jsonify({'error':True,'message':'No existe el grupo que estas tratando de editar'})

            if user.validate_group(group.id): 
                valid_name, name_message = Grupos.validate_name(name)
                valid_desc, desc_message = Grupos.validate_desc(desc)
                
                if not valid_name:
                    return jsonify({'error':True, 'message': name_message})
                if not valid_desc:
                    return jsonify({'error':True, 'message': desc_message})
                else:
                    group.nombre = name
                    group.descripcion = desc
                    group.save()  
                    return jsonify({'error':False, 'message':'Grupo editado exitosamente'})

            else:
                return jsonify({'error':True, 'message':'No tienes permisos suficientes para modificar este grupo'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Disable group
@api_user.route("/admin_groups/<int:id_grupo>/delete", methods=['DELETE'])
@administrador_required
def delete_group_api(id_grupo):
    if request.method == 'DELETE':
        try:
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)
            
            if not group:
                return jsonify({'error':True, 'message':'No existe el grupo que estas tratando de visualizar'})

            #Check if the group belongs to a teacher registered by the current user
            if user.validate_group(id_grupo):
                group.activo = False
                group.save()
                return jsonify({'error':False, 'message':'Grupo eliminado exitosamente'})
            else:
                return jsonify({'error':True, 'message':'No tienes los permisos suficientes para realizar esta operación'})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Get x group students. Using administrator user
@api_user.route("/admin_groups/<int:id_grupo>/students", methods=['GET'])
@administrador_required
def get_group_students_api(id_grupo):
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)

            if not group:
                return jsonify({'error':True, 'message':'No existe el grupo que estas tratando de visualizar'})
        
            #Check if the group belongs to a teacher registered by the current user
            if user.validate_group(id_grupo):
                students = Grupo_alumno.get_students_enrolled(id_grupo)
                return jsonify({'error':False, 'students':students})
            else:
                return jsonify({'error':True, 'message':'No tienes permisos suficientes para acceder a los estudiantes de este grupo'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Remove student from x group. Using administator user
@api_user.route("/admin_groups/<int:group>/remove_student/<int:student>", methods=['DELETE'])
@administrador_required
def remove_student_api(group, student):
    if request.method == 'DELETE':
        try:
            user = Users.get_by_id(g.user.id)

            if user.validate_group(group):
                register = Grupo_alumno.get_by_id(student, group)

                if register:
                    register.delete()
                    return jsonify({'error': False, 'message':'Alumno removido del grupo exitosamente'})
                else:
                    return jsonify({'error': True, 'message':'El alumno que estas tratando de remover del grupo, no esta registrado'})
            else:
                return jsonify({'error': True, 'message':'No tienes permisos suficientes para modifcar este grupo'})

        except KeyError:
            return jsonify({'error': True, 'message': 'Clave inválida en la solicitud'})
        except ValueError:
            return jsonify({'error': True, 'message': 'Valor inválido en la solicitud'})
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Add student to x group. Using administrator user
@api_user.route("/admin_groups/<int:id_grupo>/add_student", methods=['GET','POST'])
@administrador_required
def add_student_api(id_grupo):
    #Recover the students who are able to suscribe into the group
    if request.method == 'GET':
        grupo = Grupos.get_by_id(id_grupo)

        if not grupo:
            return jsonify({'error': True, 'message':'Grupo inexistente'})
            
        #Get teacher students and enrolled students
        students = Alumnos.get_teacher_students(grupo.id_maestro)
        enrolled_students = Grupo_alumno.get_students_enrolled(id_grupo)

        #Get primary key from enrolled students
        enrolled_student_ids = [student['student_id'] for student in enrolled_students]

        #Filter enrolled students
        filtered_students = [student for student in students if student['id'] not in enrolled_student_ids and student['activo'] == True]

        return jsonify({'error': False, 'students':filtered_students})
    
    if request.method == 'POST':
        try: 
            student_id = request.form['student']
            student = Alumnos.get_by_id(student_id)
            group = Grupos.get_by_id(id_grupo)
            user = Users.get_by_id(g.user.id)
            
            if user.validate_group(group.id):
                if not student:
                    return jsonify({'error': True, 'message':'Estudiante no existente'})
                
                if not group:
                    return jsonify({'error': True, 'message':'Grupo no existente'})
                    
                grupo_alumno = Grupo_alumno(student.id, group.id)
                grupo_alumno.save()
                return jsonify({'error': False, 'message':'Estudiante registrado exitosamente'})
            else:
                return jsonify({'error': True, 'message':'No tienes permisos suficientes para modifcar este grupo'})

        except KeyError:
            return jsonify({'error': True, 'message': 'Clave inválida en la solicitud'})
        except ValueError:
            return jsonify({'error': True, 'message': 'Valor inválido en la solicitud'})
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

#Search group by name. Only into the groups created by the teachers registered by the current user logged   
@api_user.route('/admin_groups/search', methods=['GET'])
@administrador_required
def search_group():
    if request.method == 'GET':
        # try:
        try:
            term = request.args['term']
            user = Users.get_by_id(g.user.id)
            #Get the teachers registered by the current user
            my_teachers = user.get_user_teachers()

            #List to save the groups
            groups = []

            for teacher in my_teachers: 
                #Recover the groups owned by the current teacher
                my_groups = Grupos.get_groups(teacher.id)
                groups.extend(my_groups)

            groups = [group._asdict() for group in groups if term.lower() in group.nombre.lower()]

            return jsonify({'error':False, 'groups':groups})
        except Exception as e:
            return jsonify({'error':True, 'message': 'Error al procesar la solicitud', 'exception':str(e)})

#Search enrolled students into x group. Only into the groups created by the teachers registered by the current user logged   
@api_user.route('/admin_groups/<int:id_grupo>/students/search', methods=['GET'])
@administrador_required
def search_group_student(id_grupo):    
    if request.method == 'GET':
        try:
            term = request.args['term']
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)

            if not group: 
                return jsonify({'error':True, 'message':'No existe el grupo estas tratando de visualizar'})

            if user.validate_group(id_grupo):
                students = Grupo_alumno.get_students_enrolled(id_grupo)
                students = [student for student in students if term.lower() in student['student_username'].lower()]                
                return jsonify({'error':False, 'students':students})
            else:
                return jsonify({'error':True, 'message':'No tienes permisos suficientes para acceder a los estudiantes de este grupo'})

        except Exception as e: 
            return jsonify({'error':True, 'message': 'Error al procesar la solicitud', 'exception':str(e)})

#Search not enrolled students itno x group. Only into the groups created by the teachers registered by the current user logged   
@api_user.route('/admin_groups/<int:id_grupo>/add_students/search', methods=['GET'])
@administrador_required
def search_group_available_student(id_grupo):    
    if request.method == 'GET':
        try:
            term = request.args['term']
            user = Users.get_by_id(g.user.id)
            group = Grupos.get_by_id(id_grupo)

            if not group: 
                return jsonify({'error':True, 'message':'No existe el grupo estas tratando de visualizar'})

            if user.validate_group(id_grupo):
                #Get teacher students and enrolled students
                students = Alumnos.get_teacher_students(group.id_maestro)
                enrolled_students = Grupo_alumno.get_students_enrolled(id_grupo)

                #Get primary key from enrolled students
                enrolled_student_ids = [student['student_id'] for student in enrolled_students]

                #Filter enrolled students
                filtered_students = [student for student in students if student['id'] not in enrolled_student_ids]

                #Filter by search_term
                search = [student for student in filtered_students if term.lower() in student['username'].lower()]

                return jsonify({'error':False, 'students':search})
            else:
                return jsonify({'error':True, 'message':'No tienes permisos suficientes para acceder a los estudiantes de este grupo'})

        except Exception as e: 
            return jsonify({'error':True, 'message': 'Error al procesar la solicitud', 'exception':str(e)})

#As an administrador, on admin_images, retrieve the next 20 images to show 
@api_user.route('/admin_images/next_images', methods=['GET'])
@login_user_web_required
def next_images():
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            if user.rol == 'administrador':
                current_image = int(request.args['current_image'])
                next_image = int(current_image) + 20
                new_end_image = 0

                #Get the teachers registered by the current user
                my_teachers = user.get_user_teachers()

                #List to save all the images available to edit by the current admin logged
                imagenes = []

                #Get teachers groups ids
                group_ids = [group.id for teacher in my_teachers for group in Grupos.get_groups(teacher.id)]

                #Get images uploaded in each teacher group
                for group_id in group_ids:
                    images = Imagenes_escaneadas.get_dict_images_by_group(group_id)
                    imagenes.extend(images)
                
                images_num = len(imagenes)
                rest_images = images_num - current_image

                if rest_images <= 0:
                    return jsonify({'error':True, 'message': 'No existen más imágenes para mostrar'})

                #Get the next images to show
                if rest_images > 20:
                    imagenes = imagenes[current_image:next_image]
                    new_end_image = next_image
                else:
                    imagenes = imagenes[current_image:]
                    new_end_image = images_num

                #Convert to dict each image record
                imagenes_list = [imagen._asdict() for imagen in imagenes]

            elif user.rol == 'supervisor':
                current_image = int(request.args['current_image'])
                next_image = int(current_image) + 20
                new_end_image = 0

                imagenes = []
                imagenes = Imagenes_escaneadas.get_all_images()

                images_num = len(imagenes) 
                rest_images = images_num - current_image

                if rest_images <= 0:
                    return jsonify({'error': True, 'message': 'No existen más imágenes para mostrar'})
                
                #Get the next images to show 
                if rest_images > 20:
                    imagenes = imagenes[current_image:next_image]
                    new_end_image = next_image
                else:
                    imagenes = imagenes[current_image:]
                    new_end_image = images_num

                imagenes_list = []
                for imagen in imagenes:
                    imagen_aux = {
                        'id': imagen.id,
                        'ruta': imagen.ruta,
                        'clasificacion_correcta': imagen.clasificacion_correcta,
                        'group': imagen.grupo.nombre,
                        'alumno': imagen.user_alumno.username if imagen.id_alumno is not None else '',
                        'maestro': imagen.user_maestro.username if imagen.id_maestro is not None else '',
                        'objeto': imagen.objeto_clasificado.objeto,
                        'riesgo': imagen.objeto_clasificado.incidencia.nombre
                    }
                    imagenes_list.append(imagen_aux)
         
            return jsonify({'error':False, 'images':imagenes_list, 'begin': current_image+1, 'end':new_end_image})
        except Exception as e:
            return jsonify({'error':True, 'message': 'Error al procesar la solicitud', 'exception':str(e)})

#As an administrador, on admin_images, retrieve the previous 20 images to show
@api_user.route('/admin_images/previous_images', methods=['GET'])
@login_user_web_required
def previous_image():
    if request.method == 'GET':
        try:
            user = Users.get_by_id(g.user.id)
            if user.rol == 'administrador':
                current_image = int(request.args['current_image'])
                previous_image = int(current_image) - 20

                #Get the teachers registered by the current user
                user = Users.get_by_id(g.user.id)
                my_teachers = user.get_user_teachers()

                #List to save all the images available to edit by the current admin logged
                imagenes = []

                #Get teachers groups ids
                group_ids = [group.id for teacher in my_teachers for group in Grupos.get_groups(teacher.id)]

                #Get images uploaded in each teacher group
                for group_id in group_ids:
                    images = Imagenes_escaneadas.get_dict_images_by_group(group_id)
                    imagenes.extend(images)

                if previous_image <= 0:
                    return jsonify({'error':True, 'message': 'No existen más imágenes para mostrar'})

                imagenes = imagenes[previous_image-1:current_image-1]

                #Convert to dict each image record
                imagenes_list = [imagen._asdict() for imagen in imagenes]

            elif user.rol == 'supervisor':
                current_image = int(request.args['current_image'])
                previous_image = int(current_image) - 20

                imagenes = Imagenes_escaneadas.get_all_images()

                if previous_image <= 0:
                    return jsonify({'error':True, 'message': 'No existen más imágenes para mostrar'})

                imagenes = imagenes[previous_image-1:current_image-1]

                imagenes_list = []
                for imagen in imagenes:
                    imagen_aux = {
                        'id': imagen.id,
                        'ruta': imagen.ruta,
                        'clasificacion_correcta': imagen.clasificacion_correcta,
                        'group': imagen.grupo.nombre,
                        'alumno': imagen.user_alumno.username if imagen.id_alumno is not None else '',
                        'maestro': imagen.user_maestro.username if imagen.id_maestro is not None else '',
                        'objeto': imagen.objeto_clasificado.objeto,
                        'riesgo': imagen.objeto_clasificado.incidencia.nombre
                    }
                    imagenes_list.append(imagen_aux)
                print(imagenes_list)
            return jsonify({'error':False, 'images':imagenes_list, 'begin': previous_image,'end':current_image-1})

        except Exception as e:
            return jsonify({'error':True, 'message': 'Error al procesar la solicitud', 'exception':str(e)})

#As administrator, retrieve the statistic for x object in the groups belong to him teachers
@login_user_web_required
@api_user.route('/statistic/<int:id_object>', methods=['GET'])
def get_object_statistic(id_object):
    if request.method == 'GET':
        try:
            if not Objetos.get_by_id(id_object):
                return jsonify({'error':True, 'message': 'No existe el objeto que tratas de visualizar'})
            
            user = Users.get_by_id(g.user.id)

            if user.rol == "administrador":
            
                #Get the teacher user
                teachers = user.get_user_teachers()
                
                #Get my teachers groups
                group_ids = [group.id for teacher in teachers for group in Grupos.get_groups(teacher.id)]

                images = []
                for group_id in group_ids:
                    images.extend(Imagenes_escaneadas.get_images_by_group(group_id))
                
                total_images = 0
                right_images = 0
                for image in images:
                    if image.id_objeto == id_object:
                        total_images += 1
                        if image.clasificacion_correcta == True:
                            right_images += 1
                
                statistics = {
                    'total_images': total_images,
                    'right_images': right_images
                }
            
            elif user.rol == "supervisor":
                images = Imagenes_escaneadas.get_images_by_object(id_object)

                total_images = 0
                right_images = 0
                for image in images: 
                    if image.clasificacion_correcta == True:
                        right_images += 1
                    total_images += 1

                statistics = {
                    'total_images': total_images,
                    'right_images': right_images
                }
                
            return jsonify({'error': False, 'statistics': statistics})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})