from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify, flash, current_app
from app.models.Espacio import Espacio
from app.models.Clientes import Clientes
from flask_login import login_required, current_user # Importa current_user
from app import db # Asegúrate de que 'db' esté importado de tu instancia de SQLAlchemy
from functools import wraps
from werkzeug.utils import secure_filename
import os
from app import db
from functools import wraps

bp = Blueprint('admin', __name__)

# Ruta principal del administrador (Dashboard)
@bp.route('/adminmenu')
def admin_ruti():
    espacio = Espacio.query.first() 
    print(f"espacio  {espacio}")
    clientes = [c.to_dict() for c in Clientes.query.all()]
    return render_template('admin/admintt.html', espacio=espacio, clientes=clientes)

# --- CRUD para Clientes ---
@bp.route('/admin/clientes', methods=['GET'])
def listar_clientes():
    # Lógica para listar clientes (ej: desde una base de datos)
    return render_template('admin/clientes/listar.html')

@bp.route('/admin/clientes/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        # Lógica para guardar el cliente
        return redirect(url_for('listar_clientes'))
    return render_template('admin/clientes/crear.html')

@bp.route('/admin/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        # Lógica para actualizar
        return redirect(url_for('listar_clientes'))
    return render_template('admin/clientes/editar.html', id=id)
@bp.route('/eliminar_cliente/<int:client_id>', methods=['DELETE'])
@login_required # Asegura que el usuario esté logueado
def eliminar_cliente(client_id):
    cliente_a_eliminar = Clientes.query.get(client_id)

    # 1. Verificar si el cliente existe
    if not cliente_a_eliminar:
        return jsonify({"success": False, "error": f"Cliente con ID {client_id} no encontrado."}), 404

    # 2. Validar si el cliente tiene reservas.
    # Asegúrate de que tu modelo 'Clientes' tenga una relación 'reservas' (ej. db.relationship('Reserva', back_populates='cliente'))
    if cliente_a_eliminar.reservas:
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene reservas asociadas."}), 400

    # 3. Validar si el cliente tiene motos asociadas
    # Asegúrate de que tu modelo 'Clientes' tenga una relación 'motos'
    if cliente_a_eliminar.motos:
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene motos asociadas."}), 400

    # 4. Validar si el cliente tiene autos asociados
    # Asegúrate de que tu modelo 'Clientes' tenga una relación 'autos'
    if cliente_a_eliminar.autos:
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene autos asociadas."}), 400

    # Si pasa todas las validaciones (no tiene reservas, motos ni autos)
    try:
        # Opcional: Eliminar la imagen de perfil del sistema de archivos si existe
        if cliente_a_eliminar.imgper:
            # Asegúrate de que UPLOAD_FOLDER esté definido en la configuración de tu aplicación
            filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/uploads'), cliente_a_eliminar.imgper)
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"✅ Imagen de perfil {cliente_a_eliminar.imgper} eliminada del sistema de archivos.")
            else:
                print(f"ℹ️ La imagen de perfil {cliente_a_eliminar.imgper} no se encontró en el disco.")

        db.session.delete(cliente_a_eliminar)
        db.session.commit()
        return jsonify({"success": True, "message": f"Cliente con ID {client_id} eliminado correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al intentar eliminar cliente de la BD: {e}")
        return jsonify({"success": False, "error": "Error interno del servidor al eliminar cliente."}), 500

# ... (El resto de tus rutas, como admin_ruti, get_clientes_api, etc., se mantienen igual) ...

# --- Rutas similares para Parqueaderos, Espacios y Reservas ---
@bp.route('/admin/parqueaderos')
def listar_parqueaderos():
    return render_template('admin/parqueaderos/listar.html')
# ... (Agregar rutas para crear/editar/eliminar parqueaderos)
