from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.Clientes import Clientes
from app.models.Motos import Motos
from app.models.Autos import Autos
from app import db

bp = Blueprint('auth', __name__)


@bp.route('/')
def publicidad():
    return render_template('indexpb.html')


@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        namecli = request.form['nameCli']
        passworduser = request.form['passwordUser']
        
        cliente = Clientes.query.filter_by(namecli=namecli, passworduser=passworduser).first()

        if cliente:
            login_user(cliente)
            flash("Bienvenido, eres parte de GarageSegurity", "success")
            return redirect(url_for('auth.dashboard'))

        flash('Oopss!!! tus credenciales parecen ser incorrectas', 'danger')
        return redirect(url_for('auth.login'))  # recarga el formulario

    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    return render_template('login/login.html')  # muestra el formulario


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


@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        namecli = request.form['namecli']
        clave = request.form['passworduser']
        new_user =  Clientes( passworduser=clave,namecli= namecli)
        db.session.add(  new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('/login/add.html')