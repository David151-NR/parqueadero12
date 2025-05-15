from flask import Blueprint, render_template, request, redirect, url_for
from app.models.Motos import Motos
from app import db

bp = Blueprint('moto', __name__)

@bp.route('/Moto')
def index():
    Motos = Motos.query.all()   
    return render_template('moto/index.html', data=Motos)

@bp.route('/Moto/add', methods=['GET', 'POST'])
def add():
     if request.method == 'POST':
        placa = request.form['placa']
        marcaMoto =request.form['marcaMoto']
        color = request.form['color']
        
        new_auto = Motos(placa=placa, marcaMoto=marcaMoto, color=color)
        db.session.add(new_auto)
        db.session.commit()
        
        return redirect(url_for('moto.index'))

     return render_template('moto/add.html')

@bp.route('/Moto/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    Motos = Motos.query.get_or_404(id)

    if request.method == 'POST':
        Motos.placa = request.form['placa']
        Motos.marcaMoto =request.form['marcaMoto']
        Motos.color = request.form['color']
        db.session.commit()
        return redirect(url_for('moto.index'))

    return render_template('moto/edit.html', Motos=Motos)
    

@bp.route('/Moto/delete/<int:id>')
def delete(id):
    Motos = Motos.query.get_or_404(id)
    db.session.delete(Motos)
    db.session.commit()

    return redirect(url_for('moto.index'))

@bp.route('/Moto/List/<int:id>', methods=['GET', 'POST'])
def list_Moto(id):
    Clientes = Clientes.query.get_or_404(id)
    Motos = Clientes.Motos
    return render_template('moto/List.html', Clientes=Clientes)
    
    