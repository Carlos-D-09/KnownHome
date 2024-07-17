from flask import (
    Blueprint, #Permite crear modulos configurables dentro de la aplicación
    render_template, request, url_for, g, jsonify
)
from .database.Modelos.grupos import Grupos
from .database.Modelos.maestros import Maestros

from modular.auth import maestro_required

grupo = Blueprint('grupo', __name__, url_prefix='/grupo')

@grupo.route('/<int:grupo_id>', methods=['GET'])
@maestro_required
def get_group(grupo_id):
    grupo = Grupos.get_group(grupo_id, g.user.id)
    
    if grupo:
        return jsonify({'error': False, 'grupo': grupo._asdict()}), 200
    else:
        return jsonify({'error': True, 'mensaje': 'No tienes permiso para ver este grupo o no existe o esta inhabilitado'}), 403

@grupo.route('/create', methods=['POST'])
@maestro_required
def create_group():
    try:
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        
        if not nombre or nombre.strip() == "":
            return jsonify({'error': True, 'message': 'El campo nombre no puede estar vacío'})
        
        if not Grupos.is_name_unique(None, nombre):
            return jsonify({'error': True, 'message': 'El nombre del grupo ya está en uso'})
        
    except:
        return jsonify({'error':True, 'message': 'Paramestros recibidos invalidos'})
    
    grupo = Grupos(nombre, descripcion, g.user.id)

    grupo.save()
    return jsonify({'error':False, 'codigo_acceso':grupo.codigo_acceso})
    
@grupo.route('/update/<int:id_grupo>', methods=['PUT'])
@maestro_required
def update_group(id_grupo):
    grupo = Grupos.get_group(id_grupo,g.user.id)
    if not grupo:
        return jsonify({'error': True, 'mensaje': 'Grupo no encontrado o inhabilitado'}), 404
    if grupo.id_maestro != g.user.id:
        return jsonify({'error': True, 'mensaje': 'No tienes permiso para modificar este grupo'}), 403

    try:
        grupo = None 
        grupo = Grupos.get_by_id(id_grupo)

        nuevo_nombre = request.form["nombre"].strip()  
        nueva_descripcion = request.form["descripcion"]

        if not nuevo_nombre:
            return jsonify({'error': True, 'mensaje': 'El nombre del grupo no puede estar vacío'}), 400

        grupo.update(nuevo_nombre, nueva_descripcion)
        
        return jsonify({'error': False, 'mensaje': 'Grupo actualizado con éxito'}), 200
    
    except ValueError as e:
        return jsonify({'error': True, 'mensaje': str(e)}), 409
    
@grupo.route('/delete/<int:id_grupo>', methods=['DELETE'])
@maestro_required
def delete_group(id_grupo):
    grupo = Grupos.query.filter_by(id=id_grupo, id_maestro=g.user.id).first()
    
    if not grupo or not grupo.activo:
        return jsonify({'error': True, 'message': 'Grupo no encontrado o inhabilitado'}), 404

    grupo.delete()
    return jsonify({'error': False, 'message': 'Grupo desactivado con éxito'}), 200