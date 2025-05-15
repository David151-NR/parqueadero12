from app import db

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    idReserva = db.Column(db.Integer, db.ForeignKey('reserva.idReserva'))
    idEspacio = db.Column(db.Integer,db.ForeignKey('espacio.idEspacio'))
    fecha_entrada = db.Column(db.Date())
    fecha_salida = db.Column(db.Date())
    horas_parqueo = db.Column(db.Float)
    precio_hora = db.Column(db.Float)
    total = db.Column(db.Float)
    estado = db.Column(db.String(50))  # Pendiente, Pagada, etc.
    
    reserva = db.relationship("Reserva", back_populates = "factura")
    espacio = db.relationship("Espacio", back_populates = "factura")
   
    def get_id(self):
        return str(self.iduser)
    
   