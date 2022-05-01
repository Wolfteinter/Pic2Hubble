from flask import Blueprint
from flask_restful import Api

from api.app.hubble.v2_0.resources import Generator

hubble_bp_v2 = Blueprint('hubble_v2_0_bp', __name__)
api_2 = Api(hubble_bp_v2)

api_2.add_resource(Generator, '/generator')