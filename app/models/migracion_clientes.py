from app import create_app, db
from app.models.Clientes import Clientes

app = create_app()

with app.app_context():
    clientes = Clientes.query.all()
    for cliente in clientes:
        if not cliente.correo:
            cliente.correo = ""
        if not cliente.imgper:
            cliente.imgper = "default.png"
        if not cliente.rol:
            cliente.rol = "cliente"
    db.session.commit()
    print("✅ Migración completada correctamente: campos corregidos.")
