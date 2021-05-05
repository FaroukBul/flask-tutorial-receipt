import os
from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import product
    app.register_blueprint(product.bp)

    from . import client
    app.register_blueprint(client.bp)

    from . import receipt
    app.register_blueprint(receipt.bp)
    
    return app




