import datetime
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'hard to guess string'
    # JWT SETTING
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Onekeeper'
    # RESTFUL SETTING
    ERROR_404_HELP = False
    # SQLALCHEMY SETTING
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    SCRIPTS_FOLDER = os.path.join(base_dir, 'app', 'static', 'scripts')
    REPORT_FOLDER = os.path.join(base_dir, 'reports', 'pre_text')
    REPORT_DOC_FOLDER = os.path.join(base_dir, 'reports', 'doc')
    REPORT_ZIP_FOLDER = os.path.join(base_dir, 'reports', 'statics')
    UPLOAD_ZIP_FOLDER = os.path.join(base_dir, 'uploads', 'zips')
    REPORT_INIT_FOLDER = os.path.join(base_dir, 'reports', 'config')
    REPORT_FONT_FOLDER = os.path.join(base_dir, 'reports', 'font')


class DevelopmentConfig(Config):
    DEBUG = True
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
