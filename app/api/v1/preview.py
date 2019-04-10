# -*- coding: utf-8 -*-
import os
import wechatpy
from flask import Blueprint, jsonify, current_app
from flask_restful import Api, Resource, HTTPException, abort
from ...commons.ExtParser import DispatchClient
from ...commons.wx_enterprise import WeiXin
from flask_jwt_extended import jwt_required
import json
from ...commons import exceptions

bp = Blueprint('test', __name__)
api = Api(bp)


@api.resource('/')
class TestApi(Resource):
    def get(self):
        client = DispatchClient(timeout=10)
        # _ = client.member.on_duty()
        # _ = client.dispatch.ambulance_outed()
        # _ = client.member.org_info()
        _ = client.member.mem_info()
        datas = [{
                     'user_id': mem['ID'],
                     'name': mem['NAME'],
                     'department': [mem['ORG_ID']],
                     'mobile': mem['TEXT_NUM'],
                     'position': mem['TYPENAME'],
                     'gender': 0,
                     'tel': None,
                     'email': None,
                     'weixin_id': None,
                     'extattr': None,
                 }
                 for mem in _
                 if mem['TYPE'] in (10.0, 30.0, 40.0, 50.0, 80.0, 100.0)
                 and '医院' not in mem['NAME']]

        return datas
        # datas = [{'name': org['NAME'],
        #           'parent_id': 1,
        #           'order':None,
        #           'id': org['ORG_ID']}
        #          for org in _
        #          if org['TYPE'] in (10.0, 30.0) and org['ORG_ID'] != '3310216007']
        # _ = client.ambulance.ambulance_info()
        # return datas
        # abort(300)
        # raise exceptions.AccountLoadError()
        # abort(501)
        #
        # _ = WeiXin(corp=current_app.config['WECHAT_SETTING']['default']['corp_id'],
        #            secret=current_app.config['WECHAT_SETTING']['address_book']['secret'])
        # _.connect()

        # data = {
        #     'user_id': 22222,
        #     'name':'吴勇鹏二',
        #     'department':[1],
        #     'mobile':13362621869,
        #     'position':'打杂',
        #     'gender':0,
        #     'tel':None,
        #     'email':None,
        #     'weixin_id':None,
        #     'extattr':None
        # }
        # for data in datas:
        #     try:
        #         print(data['name'])
        #         print(_.createUser(data))
        #     except:
        #         print(data['name'], '++++ed')
        #         pass
        # return {'test': 'hello world'}, 200
