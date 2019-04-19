# -*- coding: utf-8 -*-

import json
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required,
    create_refresh_token, get_jwt_identity)

bp = Blueprint('auth_routes', __name__)
api = Api(bp)



@api.resource('/')
class AuthRouteApi(Resource):
    def get(self):
        return {'/form/advanced-form': { 'authority': ['admin', 'user'] }}
