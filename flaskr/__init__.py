import os
from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/flaskr.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db, init_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    from .views import home
    app.register_blueprint(home.bp)

    from .views import customer
    app.register_blueprint(customer.bp)

    from .views import product
    app.register_blueprint(product.bp)

    from .views import receipt
    app.register_blueprint(receipt.bp)

    return app




