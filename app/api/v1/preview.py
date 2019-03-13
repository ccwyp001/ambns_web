# -*- coding: utf-8 -*-
import os
import wechatpy
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, HTTPException, abort
from ...commons.ExtParser import DispatchClient
from flask_jwt_extended import jwt_required
import json
from ...commons import exceptions
bp = Blueprint('test', __name__)
api = Api(bp)


@api.resource('/')
class TestApi(Resource):
    def get(self):
        # client = DispatchClient()
        # _ = client.member.on_duty()
        # return _
        # abort(300)
        raise exceptions.AccountLoadError()
        # abort(501)
        return {'test':'hello world'}, 200
