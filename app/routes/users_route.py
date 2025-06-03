import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
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




@bp.route('/delete/<int:id>')
def delete(id):
    clientes = Clientes.query.get_or_404(id)
    db.session.delete(clientes)
    db.session.commit()

    return redirect(url_for('clientes.index'))



@bp.route('/users/<int:idCliente>/reservas')
def reservas_cliente(idCliente):
    reservas = Reserva.query.filter_by(idCliente=idCliente).all()
    # Renderizas solo el fragmento HTML para el modal con las reservas
    return render_template('reservas_cliente.html', reservas=reservas)

























