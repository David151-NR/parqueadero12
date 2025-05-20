from flask_login import UserMixin
from app import db

class Garaje(db.Model,UserMixin): 
    __tablename__ = 'garaje'
    idGaraje = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String(50), nullable=False, unique=True)  # nuevo campo
    descripcion = db.Column(db.Text, nullable=True)
    disponible = db.Column(db.Boolean, default=True)
    ubicacion = db.Column(db.String(90), nullable=False)
