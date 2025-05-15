from flask import Blueprint, render_template, request, redirect, url_for
from app.models.Autos import Autos
from app import db

bp = Blueprint('auto', __name__)

@bp.route('/auto')
def index():
    autos = Autos.query.all()   
    return render_template('autos/index.html', data=autos)

@bp.route('/Auto/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        placa = request.form['placa']
        marcaAuto =request.form['marcaAuto']
        color = request.form['color']
        #autoCliente = request.form['autosCliente']
        new_auto = Autos(Placa=placa, marcaAuto=marcaAuto, color=color)
        db.session.add(new_auto)
        db.session.commit()
        
        return redirect(url_for('autos.index'))

    return render_template('autos/add.html')

@bp.route('/Auto/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    Autos = Autos.query.get_or_404(id)

    if request.method == 'POST':
        Autos.placa = request.form['placa'] 
        Autos.marcaAuto = request.form['marcaAuto']
        Autos.color = request.form['color']
        db.session.commit()

        return redirect(url_for('autos.index'))

    return render_template('auto/edit.html', Autos=Autos)
    

@bp.route('/Auto/delete/<int:id>')
def delete(id):
    auto = Autos.query.get_or_404(id)
    db.session.delete(auto)
    db.session.commit()

    return redirect(url_for('auto.index'))


@bp.route('/Autos/List/<int:id>', methods=['GET', 'POST'])
def list_Autos(id):
    Clientes = Clientes.query.get_or_404(id)
    Autos = Clientes.autos
    return render_template('auto/List.html', Clientes=Clientes,Autos=Autos)


