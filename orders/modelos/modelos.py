from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String


db = SQLAlchemy()

class Orden(db.Model):
    __tablename__ = 'orden'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(250))
    price = db.Column(db.Integer)
    desk = db.Column(db.String(50))
    status = db.Column(db.String(50))

class OrdenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Orden
        include_relationships = True
        load_instance = True