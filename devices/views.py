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
    except Exception:
        abort(500)

    return [device.to_dict() for device in devices_list]


def get_device(device_id):
    """

    :param device_id:
    :return: Return device info
    """
    try:
        device = Device.query.filter_by(id=device_id).first()
        print('DEVIC', device)
        if device is None:
            raise ValueError
    except TimeoutError:
        abort(408)
    except ValueError:
        abort(404)
    except Exception:
        abort(500)

    return dir(device)


def post_device(device):
    """

    :param device:
    :return: Add new device
    """
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

    return NoContent, 201


def put_device(device_id, device):
    """

    :param device_id:
    :param device:
    :return:
    """
    try:
        updated_device = Device.query.filter_by(device=device_id).update(device)
        db.session.commit(updated_device)
    except TimeoutError:
        abort(400)
    except OperationalError:
        abort(503)
    except Exception:
        abort(500)

    return NoContent, 204


def delete_device(device_id):
    """

    :param device_id:
    :return: Delete device
    """
    try:
        device = Device.query.filter_by(id=device_id).first()
        if device is None:
            raise ValueError
        db.session.delete(device)
        db.session.commit()
    except TimeoutError:
        abort(408)
    except ValueError:
        abort(404)
    except Exception:
        abort(500)

    return NoContent, 204
