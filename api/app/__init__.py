import os
from http import HTTPStatus

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# from api.app.hubble.v1_0.blueprints import hubble_bp # deprecated
from api.app.hubble.v2_0.blueprints_v2 import hubble_bp_v2


def create_app(settings_module):
    app = Flask(
        __name__,
        static_folder="build", 
        static_url_path="/",
        root_path=os.path.join(os.getcwd(), "")
    )
    app.config.from_object(settings_module)

    # Capture 404 errors
    Api(app, catch_all_404s=True)

    # Disable strict mode of sufix for URLs with "/"
    app.url_map.strict_slashes = False

    app.register_blueprint(hubble_bp_v2, url_prefix='/v2')
    CORS(app)

    # Custom error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return {"message": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @app.errorhandler(405)
    def handle_405_error(e):
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED

    @app.errorhandler(403)
    def handle_403_error(e):
        return {"message": "Forbidden error"}, HTTPStatus.FORBIDDEN

    @app.errorhandler(404)
    def handle_404_error(e):
        return {"message": "Not Found error"}, HTTPStatus.NOT_FOUND