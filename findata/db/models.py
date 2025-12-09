from datetime import datetime
from sqlalchemy import Index, CheckConstraint
from .engine import db


class Entity(db.Model):
    __tablename__ = 'entity'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_rol = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relationships
    partners = db.relationship('Finpartnerts', backref='role', lazy=True)
    admins = db.relationship('Finadmin', backref='role', lazy=True)


class Finpartnerts(db.Model):

    __tablename__ = 'finpartnerts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    contry = db.Column(db.String(100))
    age = db.Column(db.Integer, CheckConstraint('age >= 18 AND age <= 120'))
    mail = db.Column(db.String(255), nullable=False, unique=True)
    pass_ = db.Column('pass', db.String(255), nullable=False)  # 'pass' is reserved in Python
    rol = db.Column(db.Integer, db.ForeignKey('entity.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    ocupation = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    

    __table_args__ = (
        Index('idx_finpartnerts_mail', 'mail'),
        Index('idx_finpartnerts_rol', 'rol'),
    )
    

class Finadmin(db.Model):
   
    __tablename__ = 'finadmin'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    pass_ = db.Column('pass', db.String(255), nullable=False)  # 'pass' is reserved in Python
    phone = db.Column(db.String(20))
    rol = db.Column(db.Integer, db.ForeignKey('entity.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index('idx_finadmin_rol', 'rol'),
    )
    
   