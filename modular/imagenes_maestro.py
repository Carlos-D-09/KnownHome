import os
from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    render_template, request, url_for, g, jsonify, current_app
)
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from datetime import datetime

from database.Modelos.imagenes_escaneadas import Imagenes_escaneadas
from database.Modelos.grupos import Grupos
from database.Modelos.grupo_alumno import Grupo_alumno
from database.Modelos.maestros import Maestros
from database.Modelos.objetos import Objetos

from auth import maestro_required

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

imagenes_maestro = Blueprint('imgs-teacher', __name__, url_prefix='/imagenes-maestro/group')

# Subir una imagen al grupo (Profesor)
@imagenes_maestro.route('/<int:group_id>/upload', methods=['POST'])
@maestro_required
def teacher_upload_image(group_id):
    if request.method == 'POST':
        try:
            teacher = Maestros.get_by_id(g.user.id)
            grupo = Grupos.get_by_id(group_id)
            
            if not grupo:
                return jsonify({'error': True, 'message': 'El grupo no existe'})

            if grupo.id_maestro != g.user.id:
                return jsonify({'error': True, 'message': 'No tiene permiso para acceder a este grupo'})

            if 'file' not in request.files:
                return jsonify({'error': True, 'message': 'Se debe mandar un archivo formato png o jpg'})

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': True, 'message': 'Imagen no seleccionada'})

            if file:
                base_filename = secure_filename(file.filename)
                name, extension = os.path.splitext(base_filename)
                
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f"maestro{teacher.id}_grupo{grupo.id}_{current_time}{extension}"
                
                save_path = os.path.join(current_app.root_path, f'static/images/maestros/{teacher.id}', new_filename)
                file.save(save_path)
                
                new_image = Imagenes_escaneadas(id_grupo=grupo.id, nombre=new_filename, ruta=f'/static/images/maestros/{teacher.id}/{new_filename}', id_maestro=teacher.id)
                new_image.save()

                img = load_img(save_path, target_size=(256, 256))
                img_array = img_to_array(img)
                img_array_normalize = np.expand_dims(img_array, axis=0)

                probs = current_app.config['MODEL'].predict(img_array_normalize)
                clase = current_app.config['OBJETOS'][np.argmax(probs, -1)[0]]

                objeto = Objetos.get_by_object(clase)

                new_image.clasificada = True
                new_image.id_objeto = objeto.id

                new_image.save()

                image_data = {
                    'image_id': new_image.id,
                    'image_path': new_image.ruta,
                    'teacher_id': new_image.user_maestro.id,
                    'object': new_image.objeto_clasificado.objeto
                }
                
                objetos = Objetos.get_all()
                objetos_list = [{'id': objeto.id, 'objeto': objeto.objeto} for objeto in objetos]

                return jsonify({'error': False, 'message': 'La fotografía ha sido subida con éxito', 'imagen':image_data, 'objetos': objetos_list})
        except Exception as e:
            return jsonify({'error': True, 'message': 'No se ha podido completar la solicitud', 'exception': str(e)})

@imagenes_maestro.route('/<int:group_id>/student-photo/evaluate-photo/<int:image_id>', methods=['GET'])
@maestro_required
def get_photo_evaluate(group_id, image_id):
    if request.method == 'GET':
        try:
            # Verificar que exista el grupo
            if not Grupos.get_by_id(group_id):
                return jsonify({'error': True, 'message': 'No existe el grupo al que tratas de acceder'})

            #Evaluar que el usuario loggeado pertenezca al grupo
            if not Grupos.get_group(group_id, g.user.id):
                return jsonify({'error': True, 'message': 'No puedes modificar las imagenes de este grupo'})

            imagen = Imagenes_escaneadas.get_by_id(image_id)

            #Verificar que la imagen pertenezca al grupo seleccionado
            if not imagen:
                return jsonify({'error': True, 'message': 'No existe la imagen que tratas de modificar'})

            if imagen.id_grupo != group_id:
                return jsonify({'error': True, 'message': 'No puedes modificar la imagen seleccionada'})

            image_data = {
                'image_id': imagen.id,
                'image_path': imagen.ruta,
                'teacher_id': imagen.user_alumno.id,
                'object': imagen.objeto_clasificado.objeto
            }

            objetos = Objetos.get_all()
            objetos_list = [{'id': objeto.id, 'objeto': objeto.objeto} for objeto in objetos]
            
            return jsonify({'error': False, 'message': 'La fotografía ha sido subida con éxito', 'imagen':image_data, 'objetos': objetos_list})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'No se ha podido completar la solicitud', 'exception': str(e)})
        
@imagenes_maestro.route('/<int:group_id>/teacher-photo/evaluate-photo/<int:image_id>', methods=['GET'])
@maestro_required
def get_teacher_photo_evaluate(group_id, image_id):
    if request.method == 'GET':
        try:
            # Verificar que exista el grupo
            if not Grupos.get_by_id(group_id):
                return jsonify({'error': True, 'message': 'No existe el grupo al que tratas de acceder'})

            #Evaluar que el usuario loggeado pertenezca al grupo
            if not Grupos.get_group(group_id, g.user.id):
                return jsonify({'error': True, 'message': 'No puedes modificar las imagenes de este grupo'})

            imagen = Imagenes_escaneadas.get_by_id(image_id)

            #Verificar que la imagen pertenezca al grupo seleccionado
            if not imagen:
                return jsonify({'error': True, 'message': 'No existe la imagen que tratas de modificar'})

            if imagen.id_grupo != group_id:
                return jsonify({'error': True, 'message': 'No puedes modificar la imagen seleccionada'})
            
            print(imagen)

            image_data = {
                'image_id': imagen.id,
                'image_path': imagen.ruta,
                'teacher_id': imagen.user_maestro.id,
                'object': imagen.objeto_clasificado.objeto
            }

            objetos = Objetos.get_all()
            objetos_list = [{'id': objeto.id, 'objeto': objeto.objeto} for objeto in objetos]
        
            return jsonify({'error': False, 'message': 'La fotografía ha sido subida con éxito', 'imagen':image_data, 'objetos': objetos_list})
        
        except Exception as e:
            return jsonify({'error': True, 'message': 'No se ha podido completar la solicitud', 'exception': str(e)})


#Autorizar una imagen dentro del grupo
@imagenes_maestro.route('/<int:group_id>/authorize-image/<int:image_id>', methods=['PUT', 'OPTIONS'])
@maestro_required
def authorize_image(group_id, image_id):
    if request.method == 'PUT':
        try:
            authorized = bool(request.json.get('authorized'))
            clasifcation = bool(request.json.get('clasification'))

            #Verificar que existe el grupo
            if not Grupos.get_by_id(group_id):
                return jsonify({'error': True, 'message': 'No existe el grupo al que tratas de acceder'})

            #Verificar que el maestro loggeado pertenezca al grupo 
            if not Grupos.get_group(group_id, g.user.id):
                return jsonify({'error': True, 'message': 'No puedes modificar las imagenes de este grupo'})

            imagen = Imagenes_escaneadas.get_by_id(image_id)

            if not imagen:
                return jsonify({'error': True, 'message': 'No existe la imagen que tratas de modificar'})

            #Verificar que la imagen pertenezca al grupo seleccionado
            if imagen.id_grupo != group_id:
                return jsonify({'error': True, 'message': 'No puedes modificar la imagen seleccionada'})

            imagen.autorizada = authorized
            imagen.clasificacion_correcta = clasifcation
            imagen.save()

            return jsonify({'error': False, 'message': 'Imagen autorizada con exito'})

        except Exception as e:
            print(str(e))
            return jsonify({'error': True, 'message': 'No se ha podido actualizar el estado de la imagen', 'exception': str(e)})
    
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

#Modificar el objeto identificado en una imagen
@imagenes_maestro.route('/<int:group_id>/update-image-object/<int:image_id>', methods=['PUT','OPTIONS'])
@maestro_required
def update_object(group_id, image_id):
    if request.method == 'PUT':
        object_id = request.json.get('new_object')

        # Verificar que existe el grupo
        if not Grupos.get_by_id(group_id):
                return jsonify({'error': True, 'message': 'No existe el grupo al que tratas de acceder'})
        
        #Verificar que el maestro loggeado pertenece al grupo
        if not Grupos.get_group(group_id, g.user.id):
            return jsonify({'error': True, 'message': 'No puede modificar las imagenes de este grupo'})

        imagen = Imagenes_escaneadas.get_by_id(image_id)

        if not imagen:
                return jsonify({'error': True, 'message': 'No existe la imagen que tratas de modificar'}) 
        
        #Verificar que la imagen pertenezca al grupo seleccionado
        if imagen.id_grupo != group_id:
            return jsonify({'error': True, 'message': 'No puedes modificar la imagen seleccionada'})

        new_object = Objetos.get_by_id(object_id)

        if not new_object:
                return jsonify({'error': True, 'message': 'Objeto nuevo no disponible para selección'})

        imagen.clasificacion_correcta = False
        imagen.id_objeto = new_object.id
        
        if new_object.id != 0:
            imagen.autorizada = True
        
        imagen.save()

        return jsonify({'error': False, 'message': 'Objeto actualizado exitosamente'})

    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    

# Ver mis fotografías dentro de un grupo
@imagenes_maestro.route('/<int:group_id>/teacher-photos', methods=['GET'])
@maestro_required
def get_my_photos(group_id):
    if request.method == 'GET':
        if not Grupos.get_group(group_id, g.user.id):
            return jsonify({'error': True, 'message': 'No puedes consultar las imagenes de este grupo'})

        images = Imagenes_escaneadas.get_teacher_images_by_group(group_id, g.user.id)
        if not images:
            return jsonify({'error': True, 'message': 'No hay imágenes disponibles en este grupo'})

        images_data = [{
            'image_id': img.id,
            'image_path': img.ruta,
            'objeto': img.objeto_clasificado.objeto if img.objeto_clasificado is not None else '',
            'incidencia': img.objeto_clasificado.incidencia.nombre if img.objeto_clasificado is not None else '',
            'user_id': img.user_maestro.id,
            'username': img.user_maestro.username,
            'authorized': img.autorizada
        } for img in images]

        print(images_data)

        return jsonify({'error': False, 'images': images_data})

# Ver alguna fotografía mía en específico dentro del grupo
@imagenes_maestro.route('/<int:group_id>/teacher-photo/<int:photo_id>', methods=['GET'])
@maestro_required
def get_teacher_photo_detail(group_id, photo_id):
    #Verificar que el maestro loggeado pertenezca al grupo en que se quiere consultar la foto
    if not Grupos.get_group(group_id, g.user.id):
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

    #Obtener la imagen
    imagen = Imagenes_escaneadas.get_by_id(photo_id)

    if not imagen: 
        return jsonify({'error':True, 'message': 'No existe la imagen'})

    #Preparar datos de la imagen para la respuesta
    imagen_data = {
        'image_id': imagen.id,
        'image_path': imagen.ruta,
        'user': imagen.user_maestro.username,
        'object': imagen.objeto_clasificado.objeto,
        'danger_level': imagen.objeto_clasificado.incidencia.nombre,
        'description': imagen.objeto_clasificado.incidencia.descripcion,
        'suggest': imagen.objeto_clasificado.incidencia.recomendacion
    }

    return jsonify({'error': False, 'image': imagen_data})

# Ver fotografías de un alumno en especifico dentro del grupo / Pueden ser vistas fotografías autorizadas y no autorizadas
@imagenes_maestro.route('/<int:group_id>/student-photos/<int:student_id>', methods=['GET'])
@maestro_required
def get_student_images(group_id, student_id):
    grupo = Grupos.get_by_id(group_id)
    if not grupo:
        return jsonify({'error': True, 'message': 'El grupo no existe'})

    if grupo.id_maestro != g.user.id:
        return jsonify({'error': True, 'message': 'No tienes permiso para acceder a las imágenes de este grupo'})

    images = Imagenes_escaneadas.get_images_by_student_and_group(Imagenes_escaneadas, student_id, group_id)

    images_data = [{
            'image_id': img.id,
            'image_path': img.ruta,
            'objeto': img.objeto_clasificado.objeto,
            'incidencia': img.objeto_clasificado.incidencia.nombre,
            'user_id': img.user_alumno.id,
            'username': img.user_alumno.username,
            'authorized': img.autorizada
        } for img in images]

    return jsonify({'error': False, 'images': images_data})

# Ver una fotografía especifica de un alumno dentro de un grupo / Pueden ser vistas fotografías autorizadas y no autorizadas
@imagenes_maestro.route('/<int:group_id>/student-photo/<int:student_id>/detail/<int:photo_id>', methods=['GET'])
@maestro_required
def get_student_photo_detail(group_id, student_id, photo_id):
    #Verificar que el maestro logeado pertenezca al grupo
    if not Grupos.get_group(group_id, g.user.id):
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})
    
    #Verificar que el alumno pertenezca al grupo de la foto que se consulta
    if not Grupo_alumno.is_student_enrolled(student_id, group_id):
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

    imagen = Imagenes_escaneadas.get_by_id(photo_id)

    if not imagen:
        return jsonify({'error': True, 'message': 'No existe la imagen'})

    #Verificar que la imagen pertenezca al grupo
    if imagen.id_grupo != group_id:
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

    imagen_data = {
        'image_id': imagen.id,
        'image_path': imagen.ruta,
        'user': imagen.user_alumno.username,
        'object': imagen.objeto_clasificado.objeto,
        'danger_level': imagen.objeto_clasificado.incidencia.nombre,
        'description': imagen.objeto_clasificado.incidencia.descripcion,
        'suggest': imagen.objeto_clasificado.incidencia.recomendacion,
    }

    return jsonify({'error': False, 'image': imagen_data})

# Eliminar imagen de un alumno en un grupo especifico
@imagenes_maestro.route('/<int:group_id>/student-photos/<int:student_id>/photo/<int:photo_id>/delete', methods=['DELETE'])
@maestro_required
def delete_student_photo(group_id, student_id, photo_id):
    grupo = Grupos.get_by_id(group_id)
    if not grupo or grupo.id_maestro != g.user.id:
        return jsonify({'error': True, 'message': 'El grupo no existe o no tiene permiso para acceder a él'})

    if not Grupo_alumno.is_student_enrolled(student_id, group_id):
        return jsonify({'error': True, 'message': 'El alumno no existe en el grupo especificado'})

    imagen = Imagenes_escaneadas.get_image_by_id_group_and_student(Imagenes_escaneadas, photo_id, group_id, student_id)
    if not imagen:
        return jsonify({'error': True, 'message': 'La imagen no existe para el alumno y grupo especificados'})

    try:
        Imagenes_escaneadas.delete(imagen)
        return jsonify({'error': False, 'message': 'Fotografía del alumno eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': True, 'message': 'Error al eliminar la fotografía del alumno', 'details': str(e)})
    
# Eliminar imagen mía (profesor)
@imagenes_maestro.route('/<int:group_id>/teacher-photo/<int:photo_id>/delete', methods=['DELETE'])
@maestro_required
def delete_my_photo(group_id, photo_id):
    grupo = Grupos.get_by_id(group_id)
    if not grupo:
        return jsonify({'error': True, 'message': 'El grupo no existe'})

    if grupo.id_maestro != g.user.id:
        return jsonify({'error': True, 'message': 'No tiene permiso para acceder a este grupo'})

    teacher_id=g.user.id
    imagen = Imagenes_escaneadas.get_specific_teacher_image(Imagenes_escaneadas, group_id, photo_id, teacher_id)
    if not imagen:
        return jsonify({'error': True, 'message': 'La imagen no existe o no tiene permiso para eliminarla'})

    try:
        imagen.delete() 
        return jsonify({'error': False, 'message': 'Fotografía eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': True, 'message': 'Error al eliminar la fotografía', 'details': str(e)})

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response