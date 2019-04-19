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
        result = client.dispatch.ambulance_outed(start_time, end_time)
        # return result

        map_list = {
            'key': 'LSH', 'lsh': 'LSH',
            'yymc': 'YYMC',
            'clid': 'CLID',
            'clmc': 'CLMC',
            'dispatchAt': 'PCSJ',
            'departureAt': 'CCSJ',
            'arrivedAt': 'DDXCSJ',
            'boardedAt': 'SCSJ',
            'finishAt': 'WCSJ',
            'returnAt': 'FZSJ',
            'nurse': 'HS', 'doctor': 'YS', 'driver': 'SJ', 'dispatcher': 'DDY',
            'station_id': 'SZFZ',
            'status': 'CLZTSM',
            'cancel_reason':'QXYY',
            'tsqk':'TSQK',
            'swdd':'SWDD',
            'fileList': [],
            'registered':'',
            'desc':'',
            'workwear':'',
            'work_cards':'',
            'medical_warehouse':'',
        }
        _ = [{
                 key: r.get(value, '') if value else value
                 for key, value in map_list.items()
                 }
             for r in result]

        return _

    def post(self):
        pass


@api.resource('/stations')
class AmbulManageStationsApi(Resource):
    def get(self):
        client = DispatchClient(timeout=10)
        org_info = client.member.org_info()

        return [{
                    'key': _['ORG_ID'],
                    'rp_name': _['NAME']
                }
                for _ in org_info if _['TYPE'] == 30.0]

    def post(self):
        pass
