import os
from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    render_template, request, url_for, g, jsonify, current_app
)
from werkzeug.utils import secure_filename
from datetime import datetime

from .database.Modelos.imagenes_escaneadas import Imagenes_escaneadas
from .database.Modelos.grupo_alumno import Grupo_alumno
from .database.Modelos.grupos import Grupos
from .database.Modelos.alumnos import Alumnos
from .database.Modelos.objetos import Objetos

from modular.auth import alumno_required

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

imagenes_alumno = Blueprint('imagenes_alumno', __name__, url_prefix='/imagenes-alumno/group')

# Comprobar la clasificación de una imagen desde postman
@imagenes_alumno.route('/test_classification', methods=['POST'])
@alumno_required
def test_classification():
    if request.method == 'POST':
        student = Alumnos.get_by_id(g.user.id)
        group_id = 7

        file = request.files['image']

        base_filename = secure_filename(file.filename)
        name, extension = os.path.splitext(base_filename)
        
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"alumno{student.id}_grupo{group_id}_{current_time}{extension}"
        
        save_path = os.path.join(current_app.root_path, f'static/images/alumnos/{student.id}', new_filename)
        file.save(save_path)
        
        new_image = Imagenes_escaneadas(id_grupo=group_id, nombre=new_filename, ruta=save_path, id_alumno=student.id)
        new_image.save()

        img = load_img(new_image.ruta, target_size=(256, 256))
        img_array = img_to_array(img)
        img_array_normalize = np.expand_dims(img_array, axis=0)

        #Obtener la prediccion del modelo
        probs = current_app.config['MODEL'].predict(img_array_normalize)
        clase = np.argmax(probs, -1)[0]
        print(clase)
        
        return jsonify({'error':False, 'clasificacion': current_app.config['OBJETOS'][clase]})

# Subir una fotografia al grupo (alumno)
@imagenes_alumno.route('/<int:group_id>/upload', methods=['POST'])
@alumno_required
def student_upload_photo(group_id):
    # try:
    student = Alumnos.get_by_id(g.user.id)

    #Check if the student is enrolled
    if not Grupo_alumno.is_student_enrolled(student.id, group_id):
        return jsonify({'error': True, 'message': 'No perteneces al grupo'})

    #Check the file type
    if 'file' not in request.files:
        return jsonify({'error': True, 'message': 'El archivo debe ser una imagen png o jpg'})
    
    #Check if the file was sent 
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': True, 'message': 'Imagen no seleccionada'})

    #Save image uploaded
    if file:
        base_filename = secure_filename(file.filename)
        name, extension = os.path.splitext(base_filename)
        
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"alumno{student.id}_grupo{group_id}_{current_time}{extension}"
        
        save_path = os.path.join(current_app.root_path, f'static/images/alumnos/{student.id}', new_filename)
        file.save(save_path)
        
        new_image = Imagenes_escaneadas(id_grupo=group_id, nombre=new_filename, ruta=f'/static/images/alumnos/{student.id}/{new_filename}', id_alumno=student.id)
        new_image.save()

        img = load_img(save_path, target_size=(256,256))
        img_array = img_to_array(img)
        img_array_normalize = np.expand_dims(img_array, axis=0)

        probs = current_app.config['MODEL'].predict(img_array_normalize)
        clase = current_app.config['OBJETOS'][np.argmax(probs, -1)[0]]

        objeto = Objetos.get_by_object(clase)

        print(clase)

        new_image.clasificada = True
        new_image.id_objeto = objeto.id

        new_image.save()

        return jsonify({'error': False, 'message': 'La fotografía ha sido subida con éxito'})

    # except Exception as e:
    #     return jsonify({'error': True, 'message': 'No se ha podido completar la solicitud', 'exception': str(e)})

# Ver fotos autorizadas y correctamente clasificadas de x estudiante dentro del grupo
@imagenes_alumno.route('/<int:group_id>/student-photos/<int:student_id>', methods=['GET'])
@alumno_required
def get_photos_student(group_id, student_id):
    if request.method == 'GET':

        # Verificar si el alumno loggeado pertenece al grupo
        if not Grupo_alumno.is_student_enrolled(g.user.id, group_id):
            return jsonify({'error': True, 'message': 'No perteneces al grupo'})
        
        # Verificar si el alumno que se desea consultar pertenece al grupo
        if not Grupo_alumno.is_student_enrolled(student_id, group_id):
            return jsonify({'error': True, 'message': 'No existe el alumno que desea consultar'})

        images = Imagenes_escaneadas.get_authorized_images_by_student_and_group(student_id, group_id)

        images_data = [{
            'image_id': img.id,
            'image_path': img.ruta,
            'objeto': img.objeto_clasificado.objeto if img.objeto_clasificado is not None else '',
            'incidencia': img.objeto_clasificado.incidencia.nombre if img.objeto_clasificado is not None else '',
            'user_id': img.user_alumno.id,
            'username': img.user_alumno.username
        } for img in images]

        return jsonify({'error': False, 'images': images_data})

# Consultar el detalle de una foto autorizada y correctamente dentro del grupo
@imagenes_alumno.route('/<int:group_id>/student-photos/<int:student_id>/detail/<int:photo_id>', methods=['GET'])
@alumno_required
def get_student_photo_detail(group_id, student_id, photo_id):
    # Verificar si el alumno loggeado pertenece al grupo de la foto que se esta consultando
    if not Grupo_alumno.is_student_enrolled(g.user.id, group_id):
        return jsonify({'error': True, 'message': 'No puedes consultar consultar la imagen de este usuario'})

    # Verificar que el alumno que tomo la foto pertenezca al grupo
    if not Grupo_alumno.is_student_enrolled(student_id, group_id):
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

    # Obtener la imagen
    imagen = Imagenes_escaneadas.get_by_id(photo_id)
    
    # Verificar si existe la foto dentro del grupo
    if not imagen:
        return jsonify({'error': True, 'message': 'No existe la imagen'})

    # Verificar que la foto pertenezca al grupo
    if imagen.id_grupo != group_id:
        return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

    # Preparar datos de la imagen para la respuesta
    imagen_data = {
        'image_id': imagen.id,
        'image_path': imagen.ruta,
        'user': imagen.user_alumno.username,
        'object': imagen.objeto_clasificado.objeto,
        'danger_level': imagen.objeto_clasificado.incidencia.nombre,
        'description': imagen.objeto_clasificado.incidencia.descripcion,
        'suggest': imagen.objeto_clasificado.incidencia.recomendacion
    }

    return jsonify({'error': False, 'image': imagen_data})

# Ver fotos autorizadas y correctamente clasificadas del maestro de x grupo
@imagenes_alumno.route('/<int:group_id>/teacher-photos/<int:teacher_id>', methods=['GET'])
@alumno_required
def get_teacher_photos(group_id, teacher_id):
    if request.method == 'GET':
        # Verificar si el alumno loggeado pertenece al grupo
        if not Grupo_alumno.is_student_enrolled(g.user.id, group_id):
            return jsonify({'error': True, 'message': 'No perteneces al grupo'})
        
        # Verificar que el maestro que se desea consultar pertenece al grupo
        if not Grupos.get_group(group_id, teacher_id):
            return jsonify({'error': True, 'message': 'El maestro no pertenece al grupo'})

        images = Imagenes_escaneadas.get_teacher_authorized_images_by_group(group_id, teacher_id)

        images_data = [{
            'image_id': img.id,
            'image_path': img.ruta,
            'objeto': img.objeto_clasificado.objeto,
            'incidencia': img.objeto_clasificado.incidencia.nombre,
            'user_id': img.user_maestro.id,
            'username': img.user_maestro.username
        } for img in images]

        return jsonify({'error': False, 'images': images_data})

# Ver una foto autorizada específica del profesor dentro del grupo
@imagenes_alumno.route('/<int:group_id>/teacher-photos/<int:teacher_id>/detail/<int:photo_id>', methods=['GET'])
@alumno_required
def get_teacher_photo_detail(group_id, teacher_id, photo_id):
    if request.method == 'GET':
        # Verificar si el alumno loggeado pertenece al grupo de la foto que se esta consultando
        if not Grupo_alumno.is_student_enrolled(g.user.id, group_id):
            return jsonify({'error': True, 'message': 'No perteneces al grupo'})

        # Verificar que el maestro que tomo la foto pertenezca al grupo
        if not Grupos.get_group(group_id, teacher_id):
            return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

        imagen = Imagenes_escaneadas.get_by_id(photo_id)
        if not imagen:
            return jsonify({'error': True, 'message': 'No existe la imagen'})

        # Verificar que la foto pertenezca al grupo
        if imagen.id_grupo != group_id:
            return jsonify({'error': True, 'message': 'No puedes consultar la imagen de este usuario'})

        imagen_data = {
            'image_id': imagen.id,
            'image_path': imagen.ruta,
            'user': imagen.user_maestro.username,
            'object': imagen.objeto_clasificado.objeto,
            'danger_level': imagen.objeto_clasificado.incidencia.nombre,
            'description': imagen.objeto_clasificado.incidencia.descripcion,
            'suggest': imagen.objeto_clasificado.incidencia.recomendacion,
        }

        return jsonify({'error': False, 'image': imagen_data})