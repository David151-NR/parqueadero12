from flask import Blueprint, render_template, request, redirect, url_for, abort
from app.models.Espacio import Espacio
from app.models.Clientes import Clientes
from flask_login import login_required, current_user
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

@bp.route('/admin/clientes/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    # Lógica para eliminar
    return redirect(url_for('listar_clientes'))

# --- Rutas similares para Parqueaderos, Espacios y Reservas ---
@bp.route('/admin/parqueaderos')
def listar_parqueaderos():
    return render_template('admin/parqueaderos/listar.html')
# ... (Agregar rutas para crear/editar/eliminar parqueaderos)
