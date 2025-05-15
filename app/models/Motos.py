from app import db

class Motos(db.Model):
    __tablename__ = 'motos'
    idMoto = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(255), unique=True, nullable=False)
    marcaMoto = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    motoCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    
    cliente = db.relationship("Clientes", back_populates = "motos")