import json
import unittest
import connexion
from app import db


class TestDeviceCase(unittest.TestCase):
    def setUp(self):
        flask_app = connexion.FlaskApp(__name__)
        flask_app.add_api('openapi.yaml')
        self.client = flask_app.app.test_client()

        self.device1 = {
            "description": "This devices monitors the computer's temperature",
            "device_status": 0,
            "hardware_version": "0.0.1",
            "location": "Building A7",
            "mac": "00:25:96:FF:FE:12:34:56",
            "manufacturer": "ncr-inc",
            "meta_data": "string",
            "name": "Sensor oxygeno",
            "serial_number": "Y0139836",
            "software_version": "0.0.1-dev"
        }

        self.device_put = {
            "description": "This devices monitors the computer's temperature",
            "device_status": 1,
            "hardware_version": "0.0.1",
            "location": "Building A7",
            "mac": "00:25:96:FF:FE:12:34:56",
            "manufacturer": "HP",
            "meta_data": "",
            "name": "O2 Sensor",
            "serial_number": "Y0139836",
            "software_version": "0.0.1-dev"
        }
        db.session.commit()
        db.drop_all()
        db.create_all()

    def test_get_devices(self):
        # Test can fetch device
        response = self.client.get('/devices')
        assert response.status_code == 200

        # Test Insert new device
        self.client.post('/devices', json=self.device1)
        response = self.client.get('/devices/1')
        data = json.loads(response.data)
        assert response.status_code == 200

        # Test device info is saved correctly
        assert data.get('blocked') == 0
        assert data.get('serial_number') == 'Y0139836'

        # Test non existing device
        response = self.client.get('/devices/100')
        assert response.status_code == 404

    def test_post_devices(self):
        response = self.client.post('/devices', json=self.device1)
        assert response.status_code == 201

    def test_put_devices(self):
        self.client.post('/devices', json=self.device1)
        response = self.client.put('/devices/1', json=self.device_put)
        assert response.status_code == 204

        # Test data was updated
        response = self.client.get('/devices/1')
        data = json.loads(response.data)
        assert data.get('manufacturer') == 'HP'

    def test_delete_devices(self):
        # Test can delete device
        self.client.post('/devices', json=self.device1)
        response = self.client.delete('/devices/1')
        assert response.status_code == 204

        # Test device not on db returns 404
        response = self.client.delete('/devices/10')
        assert response.status_code == 404


class TestProducts(unittest.TestCase):
    def setUp(self):
        flask_app = connexion.FlaskApp(__name__)
        flask_app.add_api('openapi.yaml')
        self.client = flask_app.app.test_client()

        self.product1 = {
            'name': 'Raspberry Pi',
            'description': 'Mini Linux computer'
        }

        self.product2 = {
            'name': 'NVIDIA Jetson',
            'description': 'NVIDIA mini pc with GPU'
        }

        self.product_put = {
            'name': 'Rasp Pi',
            'description': 'Linux mini pc'
        }

        db.session.commit()
        db.drop_all()
        db.create_all()

    def test_get_products(self):
        # Test can fetch products
        response = self.client.get('/products')
        assert response.status_code == 200

        # Test insert new product
        self.client.post('/products', json=self.product1)
        response = self.client.get('/products/1')
        data = json.loads(response.data)
        assert response.status_code == 200

        # Test product info is saved correctly
        assert data.get('name') == 'Raspberry Pi'
        assert data.get('description') == 'Mini Linux computer'

        # Test non existing product return 404
        response = self.client.get('/products/100')
        assert response.status_code == 404

    def test_post_products(self):
        response = self.client.post('/products', json=self.product1)
        assert response.status_code == 201

    def test_put_products(self):
        self.client.post('products', json=self.product1)
        response = self.client.put('/products/1', json=self.product_put)
        assert response.status_code == 204

        # Test data was updated
        response = self.client.get('/products/1')
        data = json.loads(response.data)
        assert data.get('name') == 'Rasp Pi'

    def test_delete_products(self):
        # Test can delete product
        self.client.post('products', json=self.product1)
        response = self.client.delete('/products/1')
        assert response.status_code == 204

        # Test product not on db returns 404
        response = self.client.delete('/products/100')
        assert response.status_code == 404
