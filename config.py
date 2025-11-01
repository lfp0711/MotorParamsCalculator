#encoding: utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'qianqin_motor_calculator_secret_key'
    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    CSRF_ENABLED = False
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'Development': DevelopmentConfig,
    'Testing': TestingConfig,
    'Production': ProductionConfig
}