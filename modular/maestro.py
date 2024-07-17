from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    render_template, request, url_for, g, jsonify
)

from .database.Modelos.maestros import Maestros
from .database.Modelos.grupos import Grupos

from modular.auth import maestro_required, administrador_required

maestro = Blueprint('maestro', __name__, url_prefix='/maestro')

@maestro.route('/', methods=['GET'])
@maestro_required
def index():
    grupos = Grupos.get_groups(g.user.id)
    grupos_list = [grupo._asdict() for grupo in grupos]
    return jsonify({'username':g.user.username,'grupos':grupos_list})

@maestro.route('/register', methods=['GET','POST'])
@administrador_required
def register():
    if request.method == 'POST':
        #Try to read the parameters form the request
        try:
            username = request.form["username"]
            password = request.form["password"]

        except:
            return jsonify({'error':True, 'message': 'Paramestros recibidos invalidos'})

        #Check uniquess of record 
        if Maestros.get_by_username(username):
            return jsonify({'error':True, 'message': 'Nombre de usuario en uso'})

        result, message = Maestros.validate_password_format(password)

        if not result:
            return jsonify({'error':True, 'message': message})

        #Create new user
        maestro = Maestros(username, password, g.user.id)
        maestro.save()
        maestro.create_directory()

        return jsonify({'error': False, 'message': 'Maestro registrado exitosamente'})

    return render_template('maestros/register.html')

@maestro.route('/my-profile', methods=['GET'])
@maestro_required
def my_profile():
    if not g.user:
        return jsonify({'error': True, 'message': 'Usuario no autenticado o no existe'}), 401

    # Formatear la fecha de created_at a 'DD-MM-YYYY'
    formatted_date = g.user.created_at.strftime('%d-%m-%Y') if g.user.created_at else 'No disponible'

    return jsonify({
        'error': False,
        'username': g.user.username,
        'created_at': formatted_date  
    })
    
@maestro.route('/update-profile', methods=['PUT'])
@maestro_required
def update_profile():
    maestro_actual = Maestros.get_by_id(g.user.id)

    nuevo_username = request.form.get('username')
    password_actual = request.form.get('password_actual') 
    nueva_password = request.form.get('password')
    confirmar_password = request.form.get('confirmar_password')

    # Verificar que se proporcionó la contraseña actual para cualquier cambio
    if not maestro_actual.verify_current_password(password_actual):
        return jsonify({'error': True, 'message': 'Contraseña actual incorrecta'}), 401

    # Verificar que al menos uno de los campos está presente
    if not nuevo_username and not nueva_password:
        return jsonify({'error': True, 'message': 'Se requiere al menos un campo (username o password) para actualizar'}), 400

    # Actualizar el username si se proporciona uno nuevo
    if nuevo_username:
        if Maestros.get_by_username(nuevo_username) and nuevo_username != maestro_actual.username:
            return jsonify({'error': True, 'message': 'Nombre de usuario en uso'}), 409
        maestro_actual.username = nuevo_username

    # Validar y actualizar la contraseña si se proporciona una nueva
    if nueva_password:
        # Asegurarse de que también se haya proporcionado confirmar_password y coincida
        if not confirmar_password or confirmar_password != nueva_password:
            return jsonify({'error': True, 'message': 'Las contraseñas no coinciden'}), 400
        
        # Validar el formato de la nueva contraseña
        resultado, mensaje = Maestros.validate_password_format(nueva_password)
        if not resultado:
            return jsonify({'error': True, 'message': mensaje}), 400
        
        # Establecer la nueva contraseña
        maestro_actual.set_password(nueva_password)

    # Guardar los cambios en el perfil del usuario
    maestro_actual.save()

    # Devolver un mensaje de éxito
    return jsonify({'error': False, 'message': 'Perfil actualizado con éxito'}), 200

@maestro.route('/update-username', methods=['PUT'])
@maestro_required
def update_username():
    maestro_actual = Maestros.get_by_id(g.user.id)
    nuevo_username = request.form.get('username')
    password = request.form.get('password')
    confirmar_password = request.form.get('confirmar_password')  # Campo adicional para confirmar la contraseña

    if password != confirmar_password:
        return jsonify({'error': True, 'message': 'Las contraseñas no coinciden'})

    if not maestro_actual.check_password(password):
        return jsonify({'error': True, 'message': 'Contraseña incorrecta'})

    valid, message = maestro_actual.validate_new_username(nuevo_username)
    if not valid:
        return jsonify({'error': True, 'message': message})

    maestro_actual.set_new_username(nuevo_username)
    return jsonify({'error': False, 'message': 'Nombre de usuario actualizado con éxito'})

@maestro.route('/update-password', methods=['PUT'])
@maestro_required
def update_password():
    maestro_actual = Maestros.get_by_id(g.user.id)
    password_actual = request.form.get('password_actual')
    nueva_password = request.form.get('nueva_password')
    confirmar_password = request.form.get('confirmar_password')

    # Confirmar que la contraseña actual es correcta
    if not maestro_actual.check_password(password_actual):
        return jsonify({'error': True, 'message': 'Contraseña actual incorrecta'})

    # Confirmar que las nuevas contraseñas coinciden
    if nueva_password != confirmar_password:
        return jsonify({'error': True, 'message': 'Las nuevas contraseñas no coinciden'})

    # Validar el formato de la nueva contraseña
    resultado, mensaje = Maestros.validate_password_format(nueva_password)
    if not resultado:
        return jsonify({'error': True, 'message': mensaje})

    # Establecer la nueva contraseña
    maestro_actual.set_new_password(nueva_password)
    return jsonify({'error': False, 'message': 'Contraseña actualizada con éxito'})