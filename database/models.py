from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Single SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
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
    inventory_number = db.Column(db.String(100), unique=True, nullable=False)
    activation_date = db.Column(db.Date, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship for logs
    logs = db.relationship('EquipmentHistory', backref='equipment', lazy=True)

class EquipmentHistory(db.Model):
    __tablename__ = 'equipment_history'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event = db.Column(db.String(255), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)  # Optional: Track which user made the change

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event = db.Column(db.String(255), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)

class Well(db.Model):
    __tablename__ = 'wells'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Well {self.name}>"
