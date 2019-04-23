# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, current_app
from flask_restful import Api, Resource, HTTPException, abort
from ...commons.ExtParser import DispatchClient
from ...models import AmbulManage, AmbulManagePictures
from flask_jwt_extended import jwt_required
import json
from ...extensions import db
from ...commons import exceptions
from ...commons.utils import paginate
import uuid
import os

bp = Blueprint('ambul_manage', __name__)
api = Api(bp)


@api.resource('/')
class AmbulManageApi(Resource):
    def get(self):
        start_time = request.args.get('date1[0]', 0)
        end_time = request.args.get('date1[1]', 0)
        currentPage = int(request.args.get('currentPage', 0))
        pageSize = int(request.args.get('pageSize', 0))
        client = DispatchClient(timeout=10)
        result = client.dispatch.ambulance_outed(start_time, end_time)
        lsh = request.args.get('lsh', '')
        sorter = request.args.get('sorter', '')
        yymc = request.args.get('yymc', '')
        station = request.args.get('station', '')
        status = request.args.get('status', '')
        # return result
        lsh_list = [r['LSH'] for r in result]
        query_result = AmbulManage.query.filter(AmbulManage.lsh.in_(lsh_list)).all()
        query_result_list = {a.lsh + a.clid :a.display() for a in query_result}


        map_list = {
            'key': 'LSH||CCXH', 'lsh': 'LSH',
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
            'cl_state': 'CLZT',
            'cancel_reason': 'QXYY',
            'tsqk': 'TSQK',
            'swdd': 'SWDD',
            'fileList': [],
            'registered': '',
            'desc': '',
            'workwear': [],
            'work_cards': [],
            'medical_warehouse': [],
        }
        _ = [{
                 key: '_'.join([str(r.get(v, '')) for v in value.split('||')])
                 if value
                 else query_result_list.get(r['LSH']+r['CLID'], {}).get(key,value)
                 for key, value in map_list.items()
                 }
             for r in result]

        if lsh:
            _ = [i for i in _ if lsh in i['lsh']]

        if yymc:
            _ = [i for i in _ if yymc in i['yymc']]

        if station:
            _ = [i for i in _ if station in i['station_id']]

        if status:
            success_state = '6.0'
            if status in success_state:
                _ = [i for i in _ if success_state in i['cl_state']]
            else:
                _ = [i for i in _ if success_state not in i['cl_state']]

        # sorter in the last
        if sorter:
            sort_k, order = sorter.split('_')
            _.sort(key=lambda l: l[sort_k], reverse=bool(order == 'descend'))
        else:
            _.sort(key=lambda l: l['key'], reverse=True)

        _paginate = paginate(_, currentPage, pageSize)

        return {
            'list': _paginate.items,
            'pagination': {
                'total': _paginate.total,
                'pageSize': _paginate.per_page,
                'current': _paginate.page,
            }
        }

    def post(self):
        data = request.json

        ambul = AmbulManage.query.filter(
            AmbulManage.clid == data['clid'],
            AmbulManage.lsh == data['lsh']
        ).first()
        if not ambul:
            ambul = AmbulManage.from_data(data)
            db.session.add(ambul)
            db.session.flush()
        else:
            ambul.is_workwear = sum([int(_) for _ in data.get('workwear')])
            ambul.note = data.get('desc')
            ambul.is_wear_work_cards = sum([int(_) for _ in data.get('work_cards')])
            ambul.is_take_medical_warehouse = sum([int(_) for _ in data.get('medical_warehouse')])
            db.session.add(ambul)
            db.session.flush()


        for i in data['fileList']:
            pic = AmbulManagePictures.query.get(i['uid'])
            if not pic and i.get('status', 0) == 'done':
                pic = AmbulManagePictures.from_data(i)
                pic.ambul_manage_id = ambul.id
                db.session.add(pic)
                db.session.flush()
        db.session.commit()

        return self.get()


@api.resource('/stations')
class AmbulManageStationsApi(Resource):
    # @jwt_required
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


@api.resource('/pic')
class AmbulManagePicApi(Resource):
    def post(self):
        file = request.files['file']
        save_name = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], save_name)
        file.save(save_path)
        if os.path.getsize(save_path) > 1024 * 1024:
            abort(415)
        return {'id':'1'}
