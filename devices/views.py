from flask import abort
from models import Device, db, DeviceSchema, Product, ProductSchema
from sqlalchemy.exc import OperationalError
from connexion import NoContent

device_schema = DeviceSchema()
device_schemas = DeviceSchema(many=True)

product_schema = ProductSchema()
product_schemas = ProductSchema(many=True)


def get_devices():
    """
    :return: List of devices
    """
    try:
        devices_list = Device.query.all()
        result = device_schemas.dump(devices_list)
    except TimeoutError:
        abort(408, "Timeout error, please try again")
    except Exception:
        abort(500)

    return result


def get_device(device_id):
    """
    :param device_id: Unique Id for device
    :return: Device info
    """
    try:
        device = Device.query.filter_by(id=device_id).first()
        result = device_schema.dump(device)
        if device is None:
            raise ValueError
    except TimeoutError:
        abort(408)
    except ValueError:
        abort(404)
    except Exception:
        abort(500)

    return result


def post_device(device):
    """
    :param device: Dictionary containing the information about the new device
    :return: Http status code
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
    :param device_id: Unique Id for device
    :param device: Dictionary containing the information about the new device
    :return: Http status code
    """
    try:
        Device.query.filter_by(id=device_id).update(device)
        db.session.commit()
    except TimeoutError:
        abort(400)
    except OperationalError:
        abort(503)
    except Exception:
        abort(500)

    return NoContent, 204


def delete_device(device_id):
    """
    :param device_id: Unique Id for device
    :return: Http status code
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


def get_products():
    """
    :return: List of products
    """
    try:
        products_list = Product.query.all()
        result = product_schemas.dump(products_list)
    except TimeoutError:
        abort(408, "Timeout error, please try again")
    except Exception:
        abort(500)

    return result


def get_product(product_id):
    """
    :param product_id: Unique Id for product
    :return: Product info
    """
    try:
        product = Product.query.filter_by(id=product_id).first()
        result = product_schema.dump(product)
        if product is None:
            raise ValueError
    except TimeoutError:
        abort(408)
    except ValueError:
        abort(404)
    except Exception:
        abort(500)

    return result


def post_product(product):
    """
    :param product: Dictionary containing info about new product
    :return: Http status code
    """
    try:
        new_product = Product(**product)
        db.session.add(new_product)
        db.session.commit()
    except TimeoutError:
        abort(400)
    except OperationalError:
        abort(503)
    except Exception:
        abort(500)

    return NoContent, 201


def put_product(product_id, product):
    """
    :param product_id: Unique product Id
    :param product: Dictionary containing updated info about product
    :return: Http code status
    """
    try:
        Product.query.filter_by(id=product_id).update(product)
    except TimeoutError:
        abort(400)
    except OperationalError:
        abort(503)
    except Exception:
        abort(500)
    return NoContent, 204


def delete_product(product_id):
    """
    :param product_id: Unique product Id
    :return: Http status code
    """
    try:
        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            raise ValueError
        db.session.delete(product)
        db.session.commit()
    except TimeoutError:
        abort(400)
    except ValueError:
        abort(404)
    except Exception:
        abort(500)

    return NoContent, 204
