import datetime
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'AmbulanceAmbulanceAmbulance'
    # JWT SETTING
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Ambulance'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(weeks=4)
    # RESTFUL SETTING
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = False
    # SQLALCHEMY SETTING
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # WECHAT SETTING
    WECHAT_BROKER_URL = 'redis://localhost:6379/1'
    WECHAT_SETTING = {
        'default': {
            'corp_id': '1'
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

    # ExtParser SETTING
    EXT_PARSER_URL = '1'

    # ProcedureAggregate SETTING
    PROCEDURE_HOST = {
        'ip': '1',
        'port': '2',
        'instance': '3',
        'user': '4',
        'pswd': '5',
    }

    UPLOAD_FOLDER = os.path.join(base_dir, 'app', 'static', 'uploads')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 120
    SQLALCHEMY_POOL_TIMEOUT = 20

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY SETTING
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
