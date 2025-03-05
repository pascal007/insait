import os

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from resources.extensions import db, jwt
from routes.routes import initialize_routes

load_dotenv()


def create_app(config_name=None):
    flask_app = Flask(__name__)
    api = Api(flask_app)
    initialize_routes(api)
    # if config_name == "testing":
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    # else:
    #     flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    #     flask_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(flask_app)
    jwt.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
