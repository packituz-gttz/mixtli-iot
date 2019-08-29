# from devices import config
import json
import unittest
import connexion
from devices.config import db


class TestDeviceCase(unittest.TestCase):
    def setUp(self):
        flask_app = connexion.FlaskApp(__name__)
        flask_app.add_api('openapi.yaml')
        self.client = flask_app.app.test_client()
        # config.app.testing = True
        # self.app = config.app.test_client()

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

        db.drop_all()
        db.create_all()
        db.session.commit()

    def test_get_devices(self):
        # Test can fetch device
        response = self.client.get('/devices')
        self.assertEqual(response.status_code, 200)

        # Test Insert new device
        response = self.client.post('/devices', json=self.device1)
        self.assertEqual(response.status_code, 201)

        # Test can get new device
        response = self.client.get('/devices/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        # Test device info is saved correctly
        self.assertEqual(data.get('blocked'), 0)
        self.assertEqual(data.get('serial_number'), 'Y0139836')
