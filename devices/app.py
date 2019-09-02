from devices.conf import Config
import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__, specification_dir=basedir)


app = connex_app.app
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# Load api specification
connex_app.add_api('openapi.yaml')

if __name__ == '__main__':
    connex_app.run(debug=True)