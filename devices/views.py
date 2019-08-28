from flask import abort
from models import Device


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


def get_device():
    pass
