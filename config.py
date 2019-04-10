import datetime
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'AmbulanceAmbulanceAmbulance'
    # JWT SETTING
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Ambulance'
    # RESTFUL SETTING
    ERROR_404_HELP = False
    # SQLALCHEMY SETTING
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # WECHAT SETTING
    WECHAT_BROKER_URL = 'redis://localhost:6379/1'
    WECHAT_SETTING = {
        'default':{
            'corp_id':'1'
        },
        'address_book': {
            'secret': '1',
        },
        'test1': {
            'agent_id': '1',
            'secret': '1'
        },
        'alarm': {
            'agent_id': '1',
            'secret': '1'
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True
    PROPAGATE_EXCEPTIONS = False
    # SQLALCHEMY SETTING
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #     os.path.join(base_dir, 'dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY SETTING
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
