from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.Reserva import Reserva
from app.models.Espacio import Espacio
from app.models.Clientes import Clientes 
from datetime import datetime
from app import db

bp = Blueprint('Tipreser', __name__)

@bp.route('/Tipo.index')
def index(): 
    return render_template('tipo_parqueadero/index.html')

# Ruta para crear un nuevo tipo de reserva
@bp.route('/reserva', methods=['POST'])
def add():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    tipo_reserva = Reserva(nombre=nombre, descripcion=descripcion)
    db.session.add(Reserva)
    db.session.commit()

    return jsonify({
        "id": tipo_reserva.id,
        "nombre": tipo_reserva.nombre,
        "descripcion": tipo_reserva.descripcion
    }), 201

# Ruta para obtener todos los tipos de reserva
@bp.route('/tipos_reserva', methods=['GET'])
def obtener_tipos_reserva():
    tipos_reserva = Reserva.query.all()
    resultados = [{"id": tipo.id, "nombre": tipo.nombre, "descripcion": tipo.descripcion} for tipo in tipos_reserva]
    return jsonify(resultados)

# Ruta para obtener un tipo de reserva por ID
@bp.route('/tipos_reserva/<int:id>', methods=['GET'])
def obtener_tipo_reserva(id):
    tipo_reserva = Reserva.query.get(id)
    if tipo_reserva:
        return jsonify({
            "id": tipo_reserva.id,
            "nombre": tipo_reserva.nombre,
            "descripcion": tipo_reserva.descripcion
        })
    return jsonify({"error": "Tipo de reserva no encontrado"}), 404

# Ruta para actualizar un tipo de reserva por ID
@bp.route('/tipos_reserva/<int:id>', methods=['PUT'])
def actualizar_tipo_reserva(id):
    tipo_reserva = Reserva.query.get(id)
    if not tipo_reserva:
        return jsonify({"error": "Tipo de reserva no encontrado"}), 404

    data = request.get_json()
    tipo_reserva.nombre = data.get('nombre', tipo_reserva.nombre)
    tipo_reserva.descripcion = data.get('descripcion', tipo_reserva.descripcion)

    db.session.commit()

    return jsonify({
        "id": tipo_reserva.id,
        "nombre": tipo_reserva.nombre,
        "descripcion": tipo_reserva.descripcion
    })

# Ruta para eliminar un tipo de reserva por ID
@bp.route('/tipos_reserva/<int:id>', methods=['DELETE'])
def eliminar_tipo_reserva(id):
    tipo_reserva = Reserva.query.get(id)
    if not tipo_reserva:
        return jsonify({"error": "Tipo de reserva no encontrado"}), 404

    db.session.delete(tipo_reserva)
    db.session.commit()

    return jsonify({"message": "Tipo de reserva eliminado"}), 200