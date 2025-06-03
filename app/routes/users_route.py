import os
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
from app.models.Clientes import Clientes
from app.models.Reserva import Reserva
from app import db


bp = Blueprint('users', __name__)

# Configuración para la subida de imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static\\imagenes')# Ruta absoluta

# Verificar que la carpeta existe, si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica si la extensión del archivo es válida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/list')
def index():
    clientes = Clientes.query.all()
    clientes_serializados = [c.to_dict() for c in clientes]
    return render_template('cliente/list.html',clientes=clientes_serializados,datausu=current_user)


@bp.route('/add/asdfasdfa', methods=['GET', 'POST'])
@login_required
def add():

    if request.method == 'POST':
        #print("📩 Datos recibidos:", request.form)
        #print("📂 Archivos recibidos:", request.files)
        namecli = request.form['namecli']
        passworduser = request.form['passworduser']
        correo = request.form.get('correo') or ""  # 🟩 ← Esto evita None en BD
        imgper = request.files['imgper']
  
        new_user = Clientes(passworduser=passworduser, namecli=namecli,correo=correo,imgper=imgper)

        # Verificar si 'img1' está en los archivos recibidos
        #if 'img1' not in request.files:
            #flash("⚠ No se encontró la imagen en la solicitud", "error")
            #return redirect(request.url)

        file = request.files['img1perf']

        #if file.filename == '':
            #flash("⚠ No se seleccionó ninguna imagen", "error")
            #return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Nombre seguro
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            print(f"📁 Guardando imagen en: {filepath}")  # Depuración

            try:
                file.save(filepath)  # Guarda la imagen
                print(f"✅ Imagen {filename} guardada correctamente")
                new_user.imgper = filename  # Guarda solo el nombre en la BD
            except Exception as e:
                print(f"❌ Error al guardar la imagen: {str(e)}")
                flash(f"❌ Error al guardar la imagen: {str(e)}", "error")

        # Guardar usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()
        flash('✅ Usuario creado correctamente')
        
        return redirect(url_for('admin.admin_ruti'))  # Redirigir a la lista de usuarios
        
    return render_template('admin/admintt.html' )   




@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cliente = Clientes.query.get_or_404(id)

    if request.method == 'POST':
        cliente.namecli = request.form['namecli']
        cliente.correo = request.form['correo']
        db.session.commit()
        return redirect(url_for('users.index'))  # Redirige a tu vista principal de clientes

    return render_template('cliente/edit.html', datauser=cliente)

# Suponiendo que estás usando Flask
# Datos de ejemplo (reemplazar con interacción real de la base de datos)
clientes_db = [
    {"idCliente": 1, "namecli": "Juan Pérez", "correo": "juan.perez@example.com"},
    {"idCliente": 2, "namecli": "María García", "correo": "maria.garcia@example.com"},
    {"idCliente": 3, "namecli": "Pedro López", "correo": "pedro.lopez@example.com"},
    {"idCliente": 4, "namecli": "Ana Martínez", "correo": "ana.martinez@example.com"},
    {"idCliente": 5, "namecli": "Carlos Ruíz", "correo": "carlos.ruiz@example.com"}
]

@bp.route('/eliminar_cliente/<int:client_id>', methods=['DELETE'])
def eliminar_cliente(client_id):
    cliente_a_eliminar = Clientes.query.get(client_id)

    # 1. Verificar si el cliente existe
    if not cliente_a_eliminar:
        return jsonify({"success": False, "error": f"Cliente con ID {client_id} no encontrado."}), 404

    # 2. Validar si el cliente tiene reservas.
    #    'cliente_a_eliminar.reservas' accederá a la lista de objetos Reserva relacionados.
    #    Si la lista no está vacía, significa que tiene al menos una reserva.
    if cliente_a_eliminar.reservas:
        # Si quisieras ser más específico sobre "reservas activas" (por ejemplo, usando un campo 'estado' en Reserva)
        # from datetime import date
        # reservas_activas = [r for r in cliente_a_eliminar.reservas if r.estado == 'activa' and r.fecha_fin >= date.today()]
        # if reservas_activas:
        # El mensaje se mantiene genérico si solo compruebas si hay CUALQUIER reserva
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene reservas asociadas."}), 400

    # 3. Validar si el cliente tiene motos asociadas
    if cliente_a_eliminar.motos:
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene motos asociadas."}), 400

    # 4. Validar si el cliente tiene autos asociados
    if cliente_a_eliminar.autos:
        return jsonify({"success": False, "error": "No se puede eliminar el cliente. Tiene autos asociados."}), 400

    # Si pasa todas las validaciones (no tiene reservas, motos ni autos)
    try:
        db.session.delete(cliente_a_eliminar)
        db.session.commit()
        return jsonify({"success": True, "message": f"Cliente con ID {client_id} eliminado correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al intentar eliminar cliente de la BD: {e}")
        return jsonify({"success": False, "error": "Error interno del servidor al eliminar cliente."}), 500


@bp.route('/users/<int:idCliente>/reservas')
def reservas_cliente(idCliente):
    reservas = Reserva.query.filter_by(idCliente=idCliente).all()
    # Renderizas solo el fragmento HTML para el modal con las reservas
    return render_template('reservas_cliente.html', reservas=reservas)

























