from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config.config import config_dict
from flask_jwt_extended import jwt_required, create_access_token, JWTManager, jwt_manager

# from .views.pasienVW import pasien_ns
# from .views.rekam_medisVW import rekam_medis_ns
# from .views.doctorVW import dokter_ns

# from .views.users import users_ns
from .views.usersVW import users_ns
from .views.courseVW import course_ns
from .views.enrollmentVW import enrollment_ns


from .utils import db, jwt
from .models import all_table
# from .models import hospital

import logging



def create_app(config=config_dict['dev']):
    logging.basicConfig(filename=r'C:\BPY_BOOTCAMP\tugasAPI\app\logs\log_flask.log', level=logging.DEBUG, format='%(asctime)s -%(name)s -%(levelname)s -%(message)s')
    logger = logging.getLogger('test_logger')
    
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    
    api = Api(
        app,
        doc = '/index',
        title = "DAY4 ASSIGNMENT",
        description= "TUGAS DAY4 Membuat API menggunakan Flask"
    )
    
    # api.add_namespace(pasien_ns)
    # api.add_namespace(rekam_medis_ns)
    # api.add_namespace(dokter_ns)

    api.add_namespace(users_ns)
    api.add_namespace(course_ns)
    api.add_namespace(enrollment_ns)

    jwt.init_app(app)
    migrate = Migrate(app, db)

    logger.debug('Initial run API Flask')

    return app