from app import db

class Autos(db.Model):
    __tablename__ = 'autos'
    idAuto = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(255), unique=True, nullable=False)
    marcaAuto = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    autoCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    
    cliente = db.relationship("Clientes", back_populates = "autos")

