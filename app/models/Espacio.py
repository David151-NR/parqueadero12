from flask_login import UserMixin
from app import db

class Espacio(db.Model): 
    __tablename__ = 'espacio'
    idEspacio = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    disponible = db.Column(db.Boolean, default=True)
    ubicacion = db.Column(db.String(90), nullable=False)
    #proximamente  estado = db.Column(db.String(90), nullable=False, default='disponible') para poder informar cuando el espacio este en mantenimiento y demas.
   