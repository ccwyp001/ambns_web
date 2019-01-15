import os

from flask import Blueprint
from flask_restful import Api, Resource


bp = Blueprint('test', __name__)
api = Api(bp)


@api.resource('/')
class TestApi(Resource):
    def get(self):

        return {'test': 'hello world'}
