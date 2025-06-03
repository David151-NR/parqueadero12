from flask import Blueprint, render_template, request, redirect, url_for,jsonify,Flask
from flask import flash
from flask_login import current_user
from datetime import datetime
from app.models.Reserva import Reserva
from app.models.Espacio import Espacio
from app.models.Clientes import Clientes
from app import db
from datetime import datetime
import pytz

bp = Blueprint('reserva', __name__)

@bp.route('/reserva/crear/<int:id_espacio>', methods=['GET', 'POST'])
def crear_reserva(id_espacio):
    espacio = Espacio.query.get_or_404(id_espacio)
    
    if request.method == 'POST':
        try:
            print(espacio)
            print("Entra al post")
            # Obtener datos del formulario
            idcliente = request.form.get('idcliente')
            correo = request.form.get('Correo')
            placa = request.form.get('Placa')
            bogota_tz = pytz.timezone('America/Bogota')
            fecha_entrada_str = datetime.now(bogota_tz)
            print(fecha_entrada_str)
            
            # Validar campos obligatorios
            if not all([idcliente, correo, placa, fecha_entrada_str]):
                flash('Todos los campos son obligatorios', 'danger')
                usersr = current_user
                return render_template('espacio/infoespacio.html', espacio=espacio,datau=usersr)
            
            # Convertir la fecha de entrada
            try:
                fecha_entrada = fecha_entrada_str
            except ValueError:
                flash('Formato de fecha inválido', 'danger')
                usersr = current_user
                return render_template('espacio/infoespacio.html', espacio=espacio,datau=usersr)
            print("11")
            # Verificar si el espacio está disponible
            if not espacio.disponible:
                print("22")
                flash('Este espacio no está disponible', 'danger')
                return redirect(url_for('espacio.list_espacios', id=espacio.idEspacio ))
                #return render_template('espacio/infoespacio.html', espacio=espacio,datau=usersr)
              
            print("2")
            
            # Crear la reserva
            reserva = Reserva(
                ubicación=espacio.ubicacion,
                idCliente=idcliente,
                idEspacio=id_espacio,
                fecha_entrada=fecha_entrada,
                placa=placa 
            )
            print("3")
            
            # Actualizar estado del espacio
            espacio.disponible = False
            print("antes de guardar en la bd")
            db.session.add(reserva)
            db.session.commit()
            
            flash('Reserva creada exitosamente!', 'success')
            return redirect(url_for('espacio.index', espacio=espacio ))
            
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash(f'Error al crear reserva: {str(e)}', 'danger')
    return render_template('espacio/infoespacio.html', espacio=espacio, datau=current_user)

@bp.route('/reserva/actualizar', methods=['POST'])
def actualizar_reserva():
    try:
        reserva_id = request.form.get('reserva_id')
        nueva_fecha_creacion = request.form.get('fecha_creacion')
        
        reserva = Reserva.query.get_or_404(reserva_id)

        # Convertir la fecha si es necesario
        if nueva_fecha_creacion:
            reserva.fecha_creacion = datetime.strptime(nueva_fecha_creacion, "%Y-%m-%d %H:%M:%S")

        db.session.commit()
        flash('Reserva actualizada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la reserva: {str(e)}', 'danger')

    return redirect(url_for('reserva.tabla_reservas_activas'))


@bp.route('/reserva/finalizar/<int:id_reserva>', methods=['POST'])
def finalizar_reserva(id_reserva):
    try:
        reserva = Reserva.query.get_or_404(id_reserva)
        espacio = Espacio.query.get_or_404(reserva.idEspacio)

        # Actualizar campos
        bogota_tz = pytz.timezone('America/Bogota')
        reserva.fecha_salida = datetime.now(bogota_tz)
        reserva.fase = 'finalizada'
        espacio.disponible = True

        horas = 0
        minutos = 0
        if reserva.fecha_entrada:
            reserva.fecha_salida = datetime.now()
            tiempo_transcurrido =  reserva.fecha_salida - reserva.fecha_entrada
            reserva.duracion_segundos = int(tiempo_transcurrido.total_seconds())
            horas = int(tiempo_transcurrido.total_seconds() // 3600)
            minutos = int((tiempo_transcurrido.total_seconds() % 3600) // 60)
    
            flash(f'Reserva finalizada correctamente. Tiempo total: {horas} horas y {minutos} minutos.', 'success')
        else:
            flash('Reserva finalizada correctamente.', 'success')
        db.session.commit() 
             
    except Exception as e:
        db.session.rollback()
        flash(f'Error al finalizar la reserva: {str(e)}', 'danger')
        
        print("horas:", horas)
        print("minutos:", minutos)
        print("mostrar_modal:", mostrar_modal=1)

    return redirect(url_for('espacio.index', horas=horas, minutos=minutos, mostrar_modal=1))

@bp.route('/reserva/tabla_activas')
def tabla_reservas_activas():
    reservas = Reserva.query.filter_by(fase='reservado').all()
    return render_template('reserva/_tabla_reservas_activas.html', reservas=reservas)

@bp.route('/reservas_por_cliente/<int:id_cliente>')
def reservas_por_cliente(id_cliente):
   
    # Ruta para obtener y mostrar las reservas de un cliente específico en un formato de tabla
    #adecuado para ser insertado en una ventana modal.
     
    # 1. Buscar el cliente (opcional, para manejo de errores o para obtener el nombre)
    cliente = Clientes.query.get(id_cliente)
    if not cliente:
        # Si el cliente no existe, puedes devolver un mensaje de error o una tabla vacía
        return "<p>Cliente no encontrado.</p>", 404 # Código de estado HTTP 404
    print(f"Cliente encontrado: {cliente.namecli}") # Añadir esta línea   

    # 2. Obtener las reservas asociadas a ese cliente
    # Suponiendo que tu modelo Reserva tiene un campo 'idCliente' que se relaciona con 'id_cliente'
    reservas = Reserva.query.filter_by(idCliente=id_cliente).all()
    print(f"Reservas encontradas para {cliente.namecli}: {len(reservas)}") # Añadir esta línea

    # 3. Renderizar una plantilla HTML ligera que contenga la tabla de reservas
    # Esta plantilla SÓLO debe contener el cuerpo de la tabla (o el contenido que quieres en el modal)
    # y NO debe extender 'baseb.html' ni tener etiquetas <html>, <head>, <body>.
    return render_template('reserva/reservas_cliente_modal_content.html',reservas=reservas,cliente_nombre=cliente.namecli)  
                           
                        



    