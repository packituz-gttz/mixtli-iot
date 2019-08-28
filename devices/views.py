from flask import abort
from models import Device
from sqlalchemy.exc import OperationalError
from models import db
from connexion import NoContent


def get_devices():
    """
    :return: List of devices
    """
    try:
        devices_list = Device.query.all()
        print("DEVICES", devices_list)
    except TimeoutError:
        abort(408, "Timeout error, please try again")

    return devices_list


def get_device(device_id):
    """

    :param device_id:
    :return: Return device info
    """
    try:
        device = Device.query.filter_by(id=device_id).first()
        print("DEV", device)
    except TimeoutError:
        abort(408)
    except Exception:
        abort(500)

    if device is None:
        abort(404)
    return device


def post_device(device):
    try:
        new_device = Device(**device)
        db.session.add(new_device)
        db.session.commit()
    except TimeoutError:
        abort(400)
    except OperationalError:
        abort(503)
    except Exception:
        abort(500)

    return NoContent, 204
