from modelos.modelos import ( Orden, OrdenSchema, db)
import requests
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from jwt import exceptions
from json import dumps

order_schema = OrdenSchema()

class VistaRoot(Resource):
    def get(self):
        return 'API-EMPANADAS CORRIENDO BIEN', 200


class VistaHealthCheck(Resource):
    def get(self):
        return 'ok', 200

class VistaObtenerOrden(Resource):    
    def get(self, id_orden):
        try:
            # verify_jwt_in_request()
            # auth_t_u = get_jwt_identity()
            if not id_orden:
                return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
            orden_buscada = Orden.query.filter_by(id=int(id_orden)).first()
            if not orden_buscada:
                return {'error': 'No existe la orden con ese identificador..'}, 404
            else:
                print(orden_buscada.item)
                return order_schema.dump(orden_buscada), 200
        except:
            return {'error': 'A ocurrido un error con el Token o ya expiro'}, 401

class VistaActualizarStatus(Resource):
    def put(self, id_orden):
        if not id_orden:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        orden_buscada = Orden.query.filter_by(id=int(id_orden)).first()
        if not orden_buscada:
            return {'error': 'No existe la orden con ese identificador..'}, 404
        data = request.get_json()
        data_ch = 0
        if 'item' in request.json:
            item = request.json['item']
            orden_buscada.item = item
            data_ch = data_ch + 1
            print('Actualizar item ->', item)
        
        if 'price' in request.json:
            price = request.json['price']
            orden_buscada.price = price
            data_ch = data_ch + 1
            print('Actualizar price ->', str(price))
        
        if 'desk' in request.json:
            desk = request.json['desk']
            orden_buscada.desk = desk
            data_ch = data_ch + 1
            print('Actualizar desk ->', desk)
        
        if 'status' in request.json:
            status = request.json['status']
            orden_buscada.status = status
            data_ch = data_ch + 1
            print('Actualizar status ->', status)

        if data_ch > 0:
            db.session.commit()
            return order_schema.dump(orden_buscada), 200
        else:
            return "Variable not found in request body"
    
class VistaCancelarOrden(Resource):
    def delete(self, id_orden):
        if not id_orden:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        orden_buscada = Orden.query.filter_by(id=int(id_orden)).first()
        if not orden_buscada:
            return {'error': 'No existe la orden con ese identificador..'}, 404
        db.session.delete(orden_buscada)
        db.session.commit()
        return 'Orden cancelada...', 202

class VistaObtenerOrdenes(Resource):
    def get(self):
        ordenes = Orden.query.all()
        return order_schema.dump(ordenes, many=True), 200

class VistaCrearOrden(Resource): 
    def post(self):
        data = request.get_json()
        item = data['item']
        price = data['price']
        desk = data['desk']
        status = 'pending'
        token = create_access_token(identity=item)
        # verificar que los datos no esten vacios
        if not item or not price or not desk or not status:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        
        orden = Orden(item=item, price=price, desk=desk, status=status)
        db.session.add(orden)
        db.session.commit()
        return {'id':orden.id, 'status':orden.status, 'token':token}, 201