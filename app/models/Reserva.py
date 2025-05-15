from flask_login import UserMixin
from app import db

class Reserva(db.Model, UserMixin): 
    __tablename__ = 'reserva'
    idReserva = db.Column(db.Integer, primary_key=True)
    ubicación = db.Column(db.String(90), nullable=False)#ubicacion como subterraneo,segundo piso ,etc.  
    estado = db.Column(db.String(90), nullable=False, default='disponible')
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())#este campo era uriginal mente  fecha_creacion
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    idEspacio = db.Column(db.Integer, db.ForeignKey('espacio.idEspacio'))
    fecha_entrada = db.Column(db.DateTime, default=db.func.now())
    fecha_salida = db.Column(db.DateTime)
    fase = db.Column(db.String(90), nullable=False, default='reservado')# O en estado finalizada
    duracion_segundos = db.Column(db.Integer) 
    # Corregir la relación para que coincida con el nombre de la clase
    cliente = db.relationship("Clientes", back_populates="reservas")