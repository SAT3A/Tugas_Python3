# from flask_restx import Namespace, Resource, fields
# from flask import request
# from flask import jsonify, json
# from http import HTTPStatus
# from flask_jwt_extended import jwt_required, create_access_token, jwt_manager
# from werkzeug.security import genrate

# from ..utils import db
# from ..models.all_table import Users
# from ..models.all_table import Course
# from ..models.all_table import Enrollment

# auth_ns = Namespace('users', description='Namespace for users')

# users_model = users_ns.model(
#     'Users',{
#         'user_id':fields.Integer(description = "ini adalah user id"),
#         'username':fields.String(description = "ini adalah username"),
#         'email':fields.String(description = "ini adalah email"),
#         'password':fields.String(description = "ini adalah password"),
#     }
# )

# @users_ns.route('/')
# class SignUp(Resource):
    
    
#     @users_ns.marshal_list_with(users_model)
#     @users_ns.doc(
#         description = "Get all users"
#     )

#     def get (self):
#         """Get All Data Users"""

#         try:
#             data_users = Users.query.all()
#             print("data berhasil diambil : ", data_users)


#             return data_users, HTTPStatus.OK
#         except Exception as e:
#             print("Error : ", e)
#             return [], HTTPStatus.BAD_REQUEST