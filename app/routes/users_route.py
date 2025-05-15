import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
from app.models.Clientes import Clientes
from app import db


bp = Blueprint('users', __name__)

# Configuración para la subida de imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static\imagenes')  # Ruta absoluta

# Verificar que la carpeta existe, si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica si la extensión del archivo es válida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/users')
def index():
    data = Clientes.query.all()
    return render_template('cliente/index.html', data=data,datausu=current_user)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        #print("📩 Datos recibidos:", request.form)
        #print("📂 Archivos recibidos:", request.files)

        namecli = request.form['namecli']
        passworduser = request.form['passworduser']
        imgper = request.form['imgper']
       
        new_user = Clientes(passworduser=passworduser, namecli=namecli, imgper="tienda.png")

        # Verificar si 'img1' está en los archivos recibidos
        #if 'img1' not in request.files:
            #flash("⚠ No se encontró la imagen en la solicitud", "error")
            #return redirect(request.url)

        file = request.files['img1']

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
        
        return redirect(url_for('users.index'))  # Redirigir a la lista de usuarios

    return render_template('usuarios/add.html')




@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    clientes = Clientes.query.get_or_404(id)

    if request.method == 'POST':
        clientes.namecli = request.form['namecli']
        clientes.correo = request.form['correo']
        db.session.commit()        
        return redirect(url_for('users.index'))

    return render_template('cliente/edit.html', datauser=clientes)



@bp.route('/delete/<int:id>')
def delete(id):
    clientes = Clientes.query.get_or_404(id)
    db.session.delete(clientes)
    db.session.commit()

    return redirect(url_for('clientes.index'))
























