from conf import Config
import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()



def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    connex_app = connexion.App(__name__)
    connex_app.add_api('openapi.yaml')

    app = connex_app.app
    app.config.from_object(Config)

    if testing is True:
        app.config['TESTING'] = True

    db.init_app(app)
    ma.init_app(app)

    if cli is True:
        migrate.init_app(app, db)

    return connex_app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
