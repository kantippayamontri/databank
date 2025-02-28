from app.app import db  # Import db from app/__init__.py

class User(db.Model):  # Define your model
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)  
    name = db.Column(db.String(255), nullable=False)  
    last_login = db.Column(db.DateTime, default=None)  
    tour = db.Column(db.Boolean, default=False, nullable=False)  

class Device(db.Model): # Define your model
    __tablename__ = 'devices'
    id = db.Column(db.BigInteger, primary_key=True)  
    name = db.Column(db.String(255), nullable=False)  
    device_type_id = db.Column(db.DateTime, default=None)  
    tour = db.Column(db.Boolean, default=False, nullable=False)  