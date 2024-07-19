from flask import (
    Blueprint,
    flash,
    g, render_template, request, url_for, redirect, abort, jsonify, session, json
)

from datetime import datetime
from auth import login_partial_required, login_user_web_required, supervisor_required, administrador_required

from database.Modelos.usuarios import Users
from database.Modelos.codigos_verificacion import Codigos_verificacion
from database.Modelos.grupos import Grupos
from database.Modelos.passwords_antiguas import Passwords_antiguas
from database.Modelos.imagenes_escaneadas import Imagenes_escaneadas
from database.Modelos.alumnos import Alumnos
from database.Modelos.maestros import Maestros
from database.Modelos.objetos import Objetos

user = Blueprint('user', __name__, url_prefix='/user')

#Index for supervisor and administrator user
@user.route("/", methods=['GET'])
@login_user_web_required
def index():
    user = Users.get_by_id(g.user.id)
    if user.rol == "administrador":
        #Objects registered and initialization of the first object stats
        objects = Objetos.get_all()
        right_object_imgs = 0
        total_object_images = 0

        #Get the teachers actives and registered by me
        teachers = user.get_user_teachers()
        teachers_count = 0
        students_count = 0
        groups_ids = []
        for teacher in teachers:
            students_count += int(teacher.alumnos_registrados)
            teachers_count += 1
            groups_ids.extend([group.id for group in Grupos.get_groups(teacher.id)])
        
        images = []
        groups_count = 0
        #Get the images uploaded on my teachers groups
        for group_id in groups_ids:
            images_aux = Imagenes_escaneadas.get_images_by_group(group_id)
            images.extend(images_aux)
            groups_count += 1

        right_images = 0
        total_images = 0
        #Count right classifications
        for image in images:
            #Get the number of images took with the first object 
            if image.id_objeto == 1:
                total_object_images += 1
                #Get the number of right classifications with the first object  
                if image.clasificacion_correcta == True:
                    right_object_imgs += 1
           
            if image.clasificacion_correcta == True:
                right_images += 1
            
            total_images += 1

        statistics = {
            'teachers': teachers_count,
            'students': students_count,
            'groups': groups_count,
            'total_images': total_images,
            'right_images': right_images
        }

        object_statistics = {
            'total_images': total_object_images,
            'right_images': right_object_imgs
        }
    
    elif user.rol == "supervisor":
        #Objects registered and initialization of the first object stats
        objects = Objetos.get_all()
        right_object_imgs = 0
        total_object_images = 0

        #Get admin actives
        admin_users = user.get_admin_users()

        #Get active teachers
        teachers_count = Maestros.get_active_number_teachers()
        students_count = Alumnos.get_active_number_students()
        groups_count = Grupos.get_active_number_groups()

        images = Imagenes_escaneadas.get_all_images()
        total_images = 0
        right_images = 0
        #Count right classifications
        for image in images:
            if image.id_objeto == 1:
                total_object_images += 1
                if image.clasificacion_correcta == True:
                    right_object_imgs += 1

            if image.clasificacion_correcta == True:
                right_images += 1
            
            total_images += 1

        statistics = {
            'teachers': teachers_count,
            'students': students_count,
            'groups': groups_count,
            'total_images': total_images,
            'right_images': right_images 
        }

        object_statistics = {
            'total_images': total_object_images,
            'right_images': right_object_imgs
        }

    return render_template('users/index.html', statistics=statistics, objects=objects, object_statistics=object_statistics)

#Show user profile
@user.route("/profile", methods=['GET'])
@login_user_web_required
def user_profile():
    user = Users.get_general_info(g.user.id)
    return render_template('users/profile.html',user = user);

#Edit username
@user.route("/profile/edit_username", methods=['PUT'])
@login_user_web_required
def edit_username():
    if request.method == 'PUT':
        try:
            form = request.get_json()
            username = form["username"]

            user_logged = Users.get_by_id(g.user.id)

            #Validate new username (format and availability)
            valid_username, message = user_logged.validate_new_username(username)

            if not valid_username:
                return jsonify({'error': True, 'message':message})
            
            user_logged.set_new_username(username)
            return jsonify({'error':False, 'message': 'Nombre de usuario modificado exitosamente'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})
            
    return redirect(url_for(user.index))

#Edit email
@user.route("/profile/edit_email", methods=['PUT'])
@login_user_web_required
def edit_email():
    if request.method == 'PUT':
        try:
            form = request.get_json()
            correo = form["email"]
        
            user_logged = Users.get_by_id(g.user.id)

            #Validate new email 
            valid_email, message = user_logged.validate_new_email(correo)

            if not valid_email:
                return jsonify({'error': True, 'message':message})
            else:
                change_email, message = user_logged.set_new_email(correo)
                if change_email:
                    return jsonify({'error':False, 'message': 'Correo modificado exitosamente, porfavor revisa tu bandeja'})
                else:
                    return jsonify({'error':True, 'message': message})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

    return redirect(url_for(user.index))

#Edit the password
@user.route("/profile/edit_password", methods=['PUT'])
@login_user_web_required
def edit_password():
    if request.method == 'PUT':
        try:
            form = request.get_json()
            current_password = form["password"]
            new_password = form["new_password"]

            user_logged = Users.get_by_id(g.user.id)

            #Validate password (format, the current password and it hasn't been used)
            valid_password, message = user_logged.validate_new_password(current_password, new_password)

            if valid_password == False:
                return jsonify({'error': True, 'message':message})
            else:
                old_password = Passwords_antiguas(user_logged.password, user_logged.id)
                old_password.save()
                user_logged.set_new_password(new_password)
                return jsonify({'error': False, 'message': 'Constraseña modificado exitosamente'})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

    return redirect(url_for(user.index))

#Route to register a user
@user.route('/register', methods=['GET','POST'])
@supervisor_required
def register():
    if request.method == 'POST':
        #Try to read the parameters form the request
        try:
            username = request.form["username"]
            correo = request.form["email"]
            password = request.form["password"]
            rol = request.form["rol"]
        
            #Check username availability
            if Users.get_by_username(username):
                return jsonify({'error':True, 'message': 'Nombre de usuario en uso, por favor escoge otro'})
            
            #Check email availability
            if Users.get_by_email(correo):
                return jsonify({'error':True, 'message': 'Correo en uso, por favor escoge otro'})

            #Check thath the received rol is a valid one
            if Users.validate_rol(rol) == False:
                return jsonify({'error': True, 'message': 'Rol invalido'})

            #Check email (format)
            valid_email = Users.validate_email_format(correo)
            if not valid_email:
                return jsonify({'error':True, 'message': 'formato de correo electrónico invalido'})

            #Check password (format and that it hasn't been used) 
            valid_password = Users.validate_password_format(password)
            if not valid_password:
                return jsonify({'error':True, 'message': 'La contraseña debe contener al menos 8 caracteres y contener una letra mayúscula, una minúscula, un símbolo y un número'})

            #Create new user
            user = Users(correo, password, username, rol)

            #Send Verification code
            result, message, codigo = Codigos_verificacion.send_verification_email(user.username, user.correo)

            if result:
                #Save the new register
                user.save()
                codigo_verificacion = Codigos_verificacion(user.correo, codigo, user.id)
                codigo_verificacion.save()

                return jsonify({'error': False, 'message': message})
            
            else:
                return jsonify({'error': True, 'message': message})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})
    
    if request.method == 'GET':
        return render_template('users/register.html')
    
    return redirect(url_for(user.index))

#Route to send again de verification code 
@user.route("/resend_verification_code", methods=['PUT'])
@login_partial_required
def resend_verification_code():
    if request.method == 'PUT':
        user = Users.get_by_id(g.user.id)
        codigo_verificacion = Codigos_verificacion.get_by_not_used(user.id)
        result, message, codigo = codigo_verificacion.resend_code()

        if result:
            codigo_verificacion.codigo = codigo
            codigo_verificacion.fecha_creacion = datetime.utcnow()
            codigo_verificacion.save()
            return jsonify({'error':False, 'message': message})
        else:
            return jsonify({'error':True, 'message': message})
    
    return redirect(url_for(user.index))

#Route to recover an email not validated
@user.route("/recover_email_not_validated", methods=['GET','PUT'])
@login_partial_required
def recover_email():
    if request.method == 'PUT':
        try:
            form = request.get_json()
            correo = form['correo']
            confirmacion_correo = form['confirmacion_correo']

            user = Users.get_by_id(g.user.id)
            if correo != confirmacion_correo:
                return jsonify({'error':True, 'message': 'Los correos no coinciden'})
            
            #Check email format
            valid_email, message = user.validate_new_email(correo)
            if not valid_email:
                return jsonify({'error':True, 'message': message})
            
            codigo_verificacion = Codigos_verificacion.get_by_not_used(user.id)

            result, message, codigo = Codigos_verificacion.send_verification_email(user.username, correo)

            if result:
                user.correo = correo
                user.save()
                codigo_verificacion.correo = user.correo
                codigo_verificacion.codigo = codigo
                codigo_verificacion.fecha_creacion = datetime.utcnow()
                codigo_verificacion.save()
                return jsonify({'error':False,'message':message})
            else:
                return jsonify({'error':True,'message':message})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

    if request.method == 'GET':
        return render_template('users/recover_email.html')
    
    return redirect(url_for(user.index))

#Route to validate an email
@user.route("/validate_email",methods=['GET', 'PUT'])
@login_partial_required
def validate_email():
    if request.method == 'PUT':
        try:
            form = request.get_json()
            codigo = form['codigo'].upper()
        
            user = Users.get_by_id(g.user.id)
            codigo_verificacion = Codigos_verificacion.get_by_not_used(user.id)
            
            diferencia_tiempo = datetime.utcnow() - codigo_verificacion.fecha_creacion

            if codigo_verificacion.codigo == codigo:
                if diferencia_tiempo.total_seconds() > 3600:
                    return jsonify({'error':True, 'message':'Código de verificación caducado, porfavor solicite uno nuevo'})
                else:
                    codigo_verificacion.used = True
                    codigo_verificacion.save()
                    user.verified = True
                    user.save()
                    return jsonify({'error':False, 'message':'Correo validado exitosamente'})
            else:
                return jsonify({'error':True, 'message':'Codigo de verificación invalido, por favor revisalo'})

        except Exception as e:
            return jsonify({'error': True, 'message': 'Error al procesar la solicitud', 'exception': str(e)})

    if request.method == "GET":    
        return render_template('users/validate_email.html')
    
    return redirect(url_for(user.index))

#Route to show all the administrator users created by the current user logged (only if it of supervisor type)
@user.route("/admin_users", methods=['GET'])
@supervisor_required
def admin_users():
    if request.method == 'GET':
        user = Users.get_by_id(g.user.id)
        users = user.get_admin_users()
        return render_template('users/admin_users.html', users = users)

    return redirect(url_for(user.index))

@user.route("/admin_teachers", methods=['GET'])
@administrador_required
def admin_teachers():
    if request.method == 'GET':
        user = Users.get_by_id(g.user.id)
        teachers = user.get_user_teachers()
        return render_template('users/admin_teachers.html', teachers = teachers)

    return redirect(url_for(user.index))

# Route to administrate all the groups creted by the teachers registered by the current user logged 
@user.route("/admin_groups", methods=['GET'])
@administrador_required
def admin_grupos():
    if request.method == 'GET':
        #Get the teachers registered by the current user
        user = Users.get_by_id(g.user.id)
        my_teachers = user.get_user_teachers()

        #List to save the groups
        grupos = []

        for teacher in my_teachers: 
            my_groups = Grupos.get_groups(teacher.id)
            grupos.extend(my_groups)
              
        return render_template('users/admin_groups.html', grupos = grupos)

@user.route("/admin_images", methods=['GET'])
@login_user_web_required
def admin_images():
    if request.method == "GET":
        #Get the teachers registered by the current user
        user = Users.get_by_id(g.user.id)

        if user.rol == 'administrador':
            my_teachers = user.get_user_teachers()

            #List to save all the images available to edit by the current admin logged
            imagenes = []

            group_ids = [group.id for teacher in my_teachers for group in Grupos.get_groups(teacher.id)]

            for group_id in group_ids:
                images = Imagenes_escaneadas.get_images_by_group(group_id)
                imagenes.extend(images)
                
        elif user.rol == 'supervisor':
            imagenes = Imagenes_escaneadas.get_all_images()

        return render_template('users/admin_images.html', images = imagenes, images_number=len(imagenes))