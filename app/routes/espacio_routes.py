from flask import Blueprint, render_template, request, redirect, url_for 
from app.models.Espacio import Espacio
from app.models.Clientes import Clientes
from app.models.Reserva import Reserva
from flask_login import login_required,current_user
from app import db

bp = Blueprint('espacio', __name__)

@bp.route('/tarifas')
def tari():
    return render_template('tarifas/tarifas.html')

# Ruta principal que muestra todos los espacios
@bp.route('/indexespacio')
def index():
    espacios = Espacio.query.all()  # Consultamos todos los espacios

    horas = request.args.get('horas', type=int)
    minutos = request.args.get('minutos', type=int)
    mostrar_modal = request.args.get('mostrar_modal', type=int)
    
    return render_template('espacio/index.html', data=espacios, espacios=espacios,
        horas=horas,
        minutos=minutos,
        mostrar_modal=mostrar_modal)

# Ruta para agregar un nuevo espacio
@bp.route('/espacio/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        numero = request.form['numero']
        descripcion = request.form['descripcion']
        ubicacion = request.form['ubicacion']
        disponible = request.form.get('disponible', 'false').lower() == 'true'
        new_espacio = Espacio(numero=numero, descripcion=descripcion, ubicacion=ubicacion, disponible=disponible)
        db.session.add(new_espacio)
        db.session.commit()
        
        return redirect(url_for('espacio.index'))

    return render_template('espacio/add.html')


# Ruta para editar un espacio existente
@bp.route('/espacio/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    espacio = Espacio.query.get_or_404(id)  # Obtenemos el espacio por ID

    if request.method == 'POST':
        espacio.numero = request.form['numero']
        espacio.descripcion = request.form['descripcion']
        espacio.Ubicación = request.form['ubicacion']
        espacio.disponible = 'True' in request.form  # Actualizamos el estado de activo
        db.session.commit()

        return redirect(url_for('espacio.index'))

    return render_template('espacio/edit.html', espacio=espacio)

# Ruta para eliminar un espacio
@bp.route('/espacio/delete/<int:id>', methods=['GET'])
def delete(id):
    espacio = Espacio.query.get_or_404(id)
    db.session.delete(espacio)
    db.session.commit()

    return redirect(url_for('espacio.index'))

# Ruta para listar los espacios de un cliente (si aplica)
@bp.route('/infoespacio/<int:id>', methods=['GET'])
@login_required
def list_espacios(id):
    espacio = Espacio.query.get_or_404(id) 
    usersr = current_user
    reserva = Reserva.query.filter_by(idEspacio=id, fase='reservado').first()
    print(reserva)
    return render_template('espacio/infoespacio.html', espacio=espacio,datau=usersr,reserva=reserva)
    