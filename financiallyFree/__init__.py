import os
import dotenv
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv('key'),
        DATABASE = os.path.join(app.instance_path, 'flask.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # * Import views routes
    from .views import views
    app.register_blueprint(views, url_prefix ='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix = '/auth')

    from . import db
    db.init_app(app)

    return app