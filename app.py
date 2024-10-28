from typing import List
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy import Column, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

# os.environ.get('SQLALCHEMY_DATABASE_URI')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app) 
ma.init_app(app) 

#========== Models ==========

service_tickets_mechanics = db.Table(
    "service_tickets_mechanics",
    Base.metadata,
    Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    Column("mechanic_id", db.ForeignKey("mechanics.id"))
)


class Customer(Base): 
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))

    #One-to-Many
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer') 


class ServiceTicket(Base): 
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_date: Mapped[date] = mapped_column(nullable=False)
    due_date: Mapped[date] = mapped_column(nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    #Many-to-One
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets') 
    #Many-to-Many
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_tickets_mechanics, back_populates='service_tickets')

class Mechanic(Base): 
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    author: Mapped[str] = mapped_column(db.String(100), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(300), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_tickets_mechanics, back_populates='mechanics') 

#========== Schemas ==========


class CustomerSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Customer

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):  
    class Meta:
        model = ServiceTicket

class MechanicSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Mechanic

customer_schema = CustomerSchema() 
customers_schema = CustomerSchema(many=True) 
service_ticket_schema = ServiceTicketSchema() 
service_tickets_schema = ServiceTicketSchema(many=True) 
mechanic_schema = MechanicSchema() 
mechanics_schema = MechanicSchema(many=True) 