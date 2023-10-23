import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_TRACK_MODIFICATION = config('SQLALCHEMY_TRACK_MODIFICATION', cast=bool)
    

class Devconfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/tugasapi7'
    SQLALCHEMY_RECORD_QUERIES = config('SQLALCHEMY_RECORD_QUERIES', cast=bool)

class Qasconfig(Config):
    pass

class Prdconfig(Config):
    pass


config_dict = {
    'dev':Devconfig,
    'qas':Qasconfig,
    'prd':Prdconfig,
}