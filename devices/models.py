from datetime import datetime
from devices.config import db
from devices.config import ma


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)


class Product(BaseModel):
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    devices = db.relationship('Device', backref='products', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.id}, name: {self.name}>'


class Device(BaseModel):
    name = db.Column(db.String(50))
    # type = db.Column() enum, string ?
    location = db.Column(db.String(300))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    device_type = db.Column(db.Integer)
    device_status = db.Column(db.SmallInteger)
    hardware_version = db.Column(db.String(50))
    software_version = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    serial_number = db.Column(db.String(100))
    mac = db.Column(db.String(50))
    description = db.Column(db.String(300))
    last_connection = db.Column(db.DateTime)
    meta_data = db.Column(db.JSON)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    blocked = db.Column(db.SmallInteger, server_default='0')

    def __repr__(self):
        return f'<Device {self.id}, name: {self.name}>'


class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
