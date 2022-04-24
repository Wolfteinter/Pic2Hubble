from flask import Blueprint
from flask_restful import Api

from api.app.hubble.v1_0.resources import Generator


hubble_bp = Blueprint('hubble_v1_0_bp', __name__)
api = Api(hubble_bp)

api.add_resource(Generator, '/v1.0/generator')