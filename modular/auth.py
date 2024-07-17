import functools 
from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    flash,  #Permite mandar mensajes de manera generica dentro de la aplicación
    render_template, request, url_for, session, current_app, redirect, g, jsonify
)

from .database.Modelos.usuarios import Users
from .database.Modelos.maestros import Maestros
from .database.Modelos.alumnos import Alumnos
from .database.Modelos.codigos_verificacion import Codigos_verificacion

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try:
            correo = request.form['email']
            password = request.form['password']
        
        except:
            return jsonify({'error':True, 'message': 'Paramestros recibidos invalidos'})
        
        #Validate email format
        if not Users.validate_email_format(correo):
            return jsonify({'error':True, 'message':'Formato de correo electrónico no valido'})

        user = Users.get_by_email(correo)

        #Validate if the user exists 
        if not user:
            return jsonify({'error':True, 'message':'Correo o contraseña invalido, revisa tus credenciales'})
        
        else:
            #Check passowrd
            if user.check_password(password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_type'] = user.rol
                return jsonify({'error':False})
            else: 
                return jsonify({'error':True, 'message':'Correo o contraseña invalido, revisa tus credenciales'})


    return render_template('auth/login.html')

@auth.route('/login_by_username', methods=['GET','POST'])
def login_by_username():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.get_by_username(username)

        #Validate if the user exists 
        if not user:
            return jsonify({'error':True, 'message':'Correo o contraseña invalido, revisa tus credenciales'})
        
        else:
            #Check passowrd
            if user.check_password(password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_type'] = user.rol
                return jsonify({'error':False})
            else: 
                return jsonify({'error':True, 'message':'Correo o contraseña invalido, revisa tus credenciales'})


    return render_template('auth/login_by_username.html')

@auth.route('/maestro/login', methods=['POST'])
def maestro_login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except KeyError:
            return jsonify({'error':True, 'message':'Parámetros recibidos inválidos'})

        if not username or not password:
            return jsonify({'error':True, 'message':'Se requieren ambos campos'})
        
        user = Maestros.get_by_username(username)

        if not user:
            return jsonify({'error':True, 'message':'Nombre de usuario o contraseña inválidos, revisa tus credenciales'})
        else:
            # Verificar si el maestro está activo
            if not user.activo:
                return jsonify({'error': True, 'message': 'Esta cuenta de maestro está desactivada'})

            if user.check_password(password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_type'] = 'maestro'
                return jsonify({'error': False, 'message': 'Sesión iniciada correctamente', 'user_type': 'maestro'})
            else: 
                return jsonify({'error':True, 'message':'Nombre de usuario o contraseña inválidos, revisa tus credenciales'})

@auth.route('/alumno/login', methods=['POST'])
def alumno_login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except KeyError:
            return jsonify({'error': True, 'message': 'Parámetros recibidos inválidos'})

        if not username or not password:
            return jsonify({'error': True, 'message': 'Se requieren ambos campos'})

        user = Alumnos.get_by_username(username)

        if not user:
            return jsonify({'error': True, 'message': 'Nombre de usuario o contraseña inválidos, revisa tus credenciales'})
        else:
            # Verificar si el alumno está activo
            if not user.activo:
                return jsonify({'error': True, 'message': 'Esta cuenta de alumno está desactivada'})

            if user.check_password(password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_type'] = 'alumno'
                return jsonify({'error': False, 'message': 'Sesión iniciada correctamente', 'user_type': 'alumno'})
            else:
                return jsonify({'error': True, 'message': 'Nombre de usuario o contraseña inválidos, revisa tus credenciales'})


@auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    # return redirect(url_for('auth.login'))
    return redirect(url_for('auth.login'))

#Return true and the username if the user is logged, return false and a message
@auth.route('/is_logged',methods=['GET'])
def is_logged():
    if g.user:
        return jsonify({'error': False, 'username':g.user['username']})
    else:
        return jsonify({'error': True, 'username':None})
        

# If the user_type match with any of the user type, return the respective user anywase return False
def get_logged_user_by_type(user_type, user_id):

    if user_type in ['administrador', 'supervisor']:
        return Users.get_general_info(user_id)
    
    if user_type == 'maestro':
        return Maestros.get_by_id(user_id)
    
    if user_type == 'alumno':
        return Alumnos.get_by_id(user_id)
    
    return False

#Return the user if it is type supervisor or admin anywase return False
def get_user_web(user_type,user_id):
    if user_type not in ['administrador', 'supervisor']:
        return False
    
    return Users.get_by_id(user_id)

#Return the user if it is type maestro
def get_user_maestro(user_type, user_id):
    if user_type == 'maestro':
        return Maestros.get_by_id(user_id)
    
    return False

#Return the user if it is type alumno.
def get_user_alumno(user_type, user_id):
    if user_type == 'alumno':
        return Alumnos.get_by_id(user_id)
    
    return False

@auth.before_app_request
def load_logged_in_user():
    g.user = None
    user_type = session.get('user_type')
    user_id = session.get('user_id')

    if user_id is not None:
        g.user = get_logged_user_by_type(user_type, user_id)

#Start decorators        

#Requires a validate logged user 
def login_user_web_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        
        user = get_user_web(session.get('user_type'), session.get('user_id'))

        if user == False:
            return redirect(url_for('auth.login'))
        
        if not user.verified:
            return redirect(url_for('user.validate_email'))
        
        return view(**kwargs)
    return wrapped_view
    

#Requires a not validate logged user
def login_partial_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        
        user = get_user_web(session.get('user_type'), session.get('user_id'))
        
        if user == False:
            return redirect(url_for('auth.login'))
        
        if user.verified:
            return redirect(url_for('user.index'))
        
        return view(**kwargs)
    return wrapped_view

#Requires a user type supervisor
def supervisor_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        
        user = get_user_web(session.get('user_type'), session.get('user_id'))
        
        if user == False or user.rol != 'supervisor':
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

#Requires a user type administrador
def administrador_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        
        user = get_user_web(session.get('user_type'), session.get('user_id'))
        
        if user == False or user.rol != 'administrador':
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

#Requieres a user type maestro
def maestro_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return jsonify({'error': True, 'message':'Requieres tener una sesión iniciada'})
        
        user = get_user_maestro(session.get('user_type'), session.get('user_id'))
        if user == False:
            return jsonify({'error': True, 'message':'No tiene los permisos necesarios'})

        return view(**kwargs)
    return wrapped_view

#Requieres a user type alumno
def alumno_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return jsonify({'error': True, 'message':'Requieres tener una sesión iniciada'})
        
        user = get_user_alumno(session.get('user_type'), session.get('user_id'))
        
        if user == False :
            return jsonify({'error': True, 'message':'No tiene los permisos necesarios'})

        return view(**kwargs)
    return wrapped_view

#End decorators
    
