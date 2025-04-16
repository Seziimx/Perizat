from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    inventory_number = db.Column(db.String(50), unique=True, nullable=False)
    activation_date = db.Column(db.Date, nullable=False)
    last_maintenance = db.Column(db.Date)
