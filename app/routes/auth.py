import os
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.models.Clientes import Clientes
from app.models.Motos import Motos
from app.models.Autos import Autos
from app import db

bp = Blueprint('auth', __name__)


@bp.route('/')
def publicidad():
    return render_template('indexPb.html')


@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        namecli = request.form['nameCli']
        password = request.form['passwordUser']

        cliente = Clientes.query.filter_by(namecli=namecli).first()

        if cliente and cliente.check_password(password):
            login_user(cliente)
            flash("Bienvenido, eres parte de GarageSegurity", "success")
            return redirect(url_for('auth.dashboard'))

        flash('Oopss!!! tus credenciales parecen ser incorrectas', 'danger')
        return redirect(url_for('auth.login'))

    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    return render_template('login/login.html')



@bp.route('/dashboard')
@login_required
def dashboard(): 
    clientes = Clientes.query.all()  
    dataprod_motos = Motos.query.all()  
    dataprod_autos = Autos.query.all()  
    return render_template("/tutorial/tutorial.html", datausu=current_user, datausers=clientes, dataprod_motos=dataprod_motos, dataprod_autos=dataprod_autos)

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/addnow', methods=['GET', 'POST'])
def addnow():
    if request.method == 'POST':
        namecli = request.form['namecli']
        clave = request.form['passworduser']
        vclave = request.form['vclaveuser']
        correo = request.form['correo']
        telefono = request.form.get('telefono')

        # Validar contraseñas
        if clave != vclave:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(request.url)

        # Verificar si ya existe un usuario con ese nombre
        if Clientes.query.filter_by(namecli=namecli).first():
            flash('Ese nombre de usuario ya está registrado.', 'warning')
            return redirect(request.url)

        # Validación y carga de imagen
        img_file = request.files.get('img1')
        if img_file and img_file.filename != '':
            filename = secure_filename(img_file.filename)
            img_path = os.path.join('static/uploads', filename)
            full_path = os.path.join(current_app.root_path, img_path)

                # Asegurarse de que la carpeta exista
            folder = os.path.dirname(full_path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            img_file.save(full_path)
        else:
            flash('Debe subir una imagen de perfil.', 'warning')
            return redirect(request.url)

        # Crear usuario
        new_user = Clientes(
            namecli=namecli,
            correo=correo,
            telefono=telefono,
            imgper=img_path
        )
        new_user.set_password(clave)  # Usamos el método del modelo

        db.session.add(new_user)
        db.session.commit()

        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('login/add.html')

