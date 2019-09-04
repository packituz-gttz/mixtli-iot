import json
import pytest
import connexion
from app import create_app
from app import db as _db
from models import Device, Product


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app.app

@pytest.fixture
def db(app):
    _db.app = app
    
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()

device_mock = {
    "description": "This devices monitors the computer's temperature",
    "device_status": 0,
    "hardware_version": "0.0.1",
    "location": "Building A7",
    "mac": "00:25:96:FF:FE:12:34:56",
    "manufacturer": "ncr-inc",
    "meta_data": "string",
    "name": "Sensor oxygen",
    "serial_number": "Y0139836",
    "software_version": "0.0.1-dev"
}

@pytest.fixture
def device_record(db):
    device = Device(**device_mock)

    db.session.add(device)
    db.session.commit()

    return device

product_mock = {
    'name': 'Raspberry Pi',
    'description': 'Mini Linux computer'
}

@pytest.fixture
def product_record(db):
    product = Product(**product_mock)

    db.session.add(product)
    db.session.commit()

    return product

def test_get_devices(client, db):
    # Test can fetch device
    response = client.get('/devices')
    assert response.status_code == 200

    with pytest.raises(Exception):
        response = client.get('/devices')
        assert response.status_code == 500

def test_get_device(client, db, device_record):
    # Test Insert new device
    response = client.get('/devices/1')
    data = json.loads(response.data)
    assert response.status_code == 200

    # Test device info is saved correctly
    assert data.get('blocked') == 0
    assert data.get('serial_number') == 'Y0139836'

    # Test non existing device
    response = client.get('/devices/100')
    assert response.status_code == 404

def test_post_devices(client, db):
    response = client.post('/devices', json=device_mock)
    assert response.status_code == 201

def test_put_devices(client, db, device_record):
    device_mock['manufacturer'] = 'HP'
    response = client.put('/devices/1', json=device_mock)
    assert response.status_code == 204

    # Test data was updated
    response = client.get('/devices/1')
    data = json.loads(response.data)
    assert data.get('manufacturer') == 'HP'

def test_delete_devices(client, db, device_record):
    # Test can delete device
    response = client.delete('/devices/1')
    assert response.status_code == 204

    # Test device not on db returns 404
    response = client.delete('/devices/1')
    assert response.status_code == 404

def test_get_products(client, db):
    # Test can fetch products
    response = client.get('/products')
    assert response.status_code == 200

def test_get_product(client, db, product_record):
    # Test insert new product
    response = client.get('/products/1')
    data = json.loads(response.data)
    assert response.status_code == 200

    # Test product info is saved correctly
    assert data.get('name') == 'Raspberry Pi'
    assert data.get('description') == 'Mini Linux computer'

    # Test non existing product return 404
    response = client.get('/products/100')
    assert response.status_code == 404

def test_post_products(client, db):
    response = client.post('/products', json=product_mock)
    assert response.status_code == 201

def test_put_products(client, db, product_record):
    product_mock['name'] = 'Rasp Pi'
    response = client.put('/products/1', json=product_mock)
    assert response.status_code == 204

    # Test data was updated
    response = client.get('/products/1')
    data = json.loads(response.data)
    assert data.get('name') == 'Rasp Pi'

def test_delete_products(client, db, product_record):
    # Test can delete product
    response = client.delete('/products/1')
    assert response.status_code == 204

    # Test product not on db returns 404
    response = client.delete('/products/1')
    assert response.status_code == 404
