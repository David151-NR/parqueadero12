from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash  # Importa estas funciones
from app import db

class Clientes(db.Model, UserMixin):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer, primary_key=True)
    namecli = db.Column(db.String(90), unique=True, nullable=False)
    passworduser = db.Column(db.String(300), nullable=False)  # Aquí se almacenará el hash
    correo = db.Column(db.String(90), nullable=True)
    imgper = db.Column(db.String(300), nullable=True)
    rol = db.Column(db.String(20), default='cliente')  # admin, gestor, cliente
    
    reservas = db.relationship("Reserva", back_populates="cliente")
    motos = db.relationship("Motos", back_populates="cliente") 
    autos = db.relationship("Autos", back_populates="cliente") 

    # Métodos para manejo seguro de contraseñas
    def set_password(self, password):
        """Genera un hash seguro de la contraseña y lo guarda en passworduser"""
        self.passworduser = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado"""
        return check_password_hash(self.passworduser, password)

    # Métodos existentes (los mantienes igual)
    def get_id(self):
        return str(self.idCliente)
    
    def get_img(self, img_attr):
        return getattr(self, img_attr) if getattr(self, img_attr) else "imagenes/usuario.png"
    
    def get_img2(self):
        """Retorna la imagen de perfil del usuario o una imagen por defecto."""
        return f"imagenes/{self.imgper}" if self.imgper else "imagenes/casco1.webp"
    
    def get_img2(self):
        """Retorna la imagen de perfil del usuario o una imagen por defecto."""
        return f"imagenes/{self.imgper}" if self.imgper else "imagenes/casco1.webp"
   