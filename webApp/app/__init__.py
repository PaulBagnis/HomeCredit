from flask_bootstrap import Bootstrap
from flask import Flask
from decouple import config
from config import config_dict

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config_dict[config("FLASK_ENV")])

    bootstrap.init_app(app)
    
    from app.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
