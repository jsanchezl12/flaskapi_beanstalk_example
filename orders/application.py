from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos.modelos import db
from datetime import timedelta
from vistas import VistaRoot, VistaHealthCheck, VistaObtenerOrden, VistaCrearOrden, VistaObtenerOrdenes, VistaActualizarStatus, VistaCancelarOrden
#DATABASE_URI = 'sqlite:///restaurants.db'
DATABASE_URI = 'postgresql+psycopg2://postgres:DreamTeam123*@database-1.cazbca9jsbii.us-east-1.rds.amazonaws.com/postgres'

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'frase-secreta-restaurante'
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

app_context = application.app_context()
app_context.push()
db.init_app(application)
db.create_all()

cors = CORS(application)

api = Api(application)
api.add_resource(VistaRoot, '/')
# HealthCheck -> GET
api.add_resource(VistaHealthCheck, '/orders/health')
# Crear Orden -> POST
api.add_resource(VistaCrearOrden, '/orders/')
# Obtener Ordenes -> GET
api.add_resource(VistaObtenerOrdenes, '/orders/')
# Obtener orden por ID -> GET
api.add_resource(VistaObtenerOrden, '/orders/<int:id_orden>')
# Actualizar orden por id -> PUT
api.add_resource(VistaActualizarStatus, '/orders/<int:id_orden>')
# Cancelar orden por id -> DELETE
api.add_resource(VistaCancelarOrden, '/orders/<int:id_orden>')

# Componente para manejar JWT
jwt = JWTManager(application)

print(' * ORDERS corriendo ----------------')

if __name__ == "__main__":
    PORT = 5001
    application.run(port=PORT, debug=True) 
