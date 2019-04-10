# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, HTTPException, abort
from ...commons.ExtParser import DispatchClient
from ...models import AmbulManage, AmbulManagePictures
from flask_jwt_extended import jwt_required
import json
from ...commons import exceptions

bp = Blueprint('ambul_manage', __name__)
api = Api(bp)


@api.resource('/')
class AmbulManageApi(Resource):
    def get(self):
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', 0)
        client = DispatchClient(timeout=10)
        _ = client.dispatch.ambulance_outed()


        return _

    def post(self):
        pass

